import django.core.exceptions

from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from cms.models import Title

from common_plugins.views import CollectionFormMixin
from pos_api.pos_client import PWAPI
from pos_api.models.pet import ApiPetPhoto
from pinogy_pet.forms import PetCollectionForm
from pinogy_pet import utils
from pinogy_pet.pos_api import APIPetTypeSetting, PetTypeList

class PetTypeView(TemplateView):
    template_name = 'pinogy_pets/pets_type_app_hook.html'
    
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        # Handling the redirection for pet type homepage
        try:
            pet_type_page_title = Title.objects.filter(page__application_urls='PetsApphook', publisher_is_draft=False).first()
            if pet_type_page_title and pet_type_page_title.redirect:
                return redirect(pet_type_page_title.redirect)
        except (Title.DoesNotExist, Exception) as e:
            pass
        
        pet_types_obj = PetTypeList()
        pet_types_list = pet_types_obj.get_pet_type_list(None)
        
        # Redirect to pet list page if only one pet type is available
        if len(pet_types_list) == 1:
            return redirect('pinogy_pet:pet_type', pet_type_slug=pet_types_list[0].slug)
        
        context = {
            'pet_types_list': pet_types_list,
        }
        return render(request, self.template_name, context)
    
class PetlistView(TemplateView):
    template_name = 'pinogy_pets/pets_list_app_hook.html'
    
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get(self, request, pet_type_slug = None, breed_slug = None, location_slug = None, *args, **kwargs):

        # Check if there is only one pet type, and set the flag accordingly
        # There is only one pet type, so we don't want to show the link in the breadcrumb
        canonical_url = f"{request.scheme}://{request.get_host()}{request.path}"
        show_pet_type_link = True
        pet_types_obj = PetTypeList()
        pet_types_list = pet_types_obj.get_pet_type_list(None)
        
        if len(pet_types_list) == 1:
            show_pet_type_link = False

        context = {
            'selected_pet_type_slug': pet_type_slug,
            'show_pet_type_link': show_pet_type_link 
        }
        
        if breed_slug:
            client = PWAPI()
            context['selected_breed_data'] = client.get_breed(breed_slug)

            # Updateing canonnical url to breed detail page
            breed_detail_page_url = reverse('pinogy_breeds:breed_detail', kwargs={'pet_type_slug': pet_type_slug, 'breed_slug': breed_slug})
            canonical_url = f"{request.scheme}://{request.get_host()}{breed_detail_page_url}"

        # If location slug is available than find location data 
        # return 404 if location does not exist
        if location_slug:
            client = PWAPI()
            locations = client.get_website_data()['locations']
            for location in locations:
                if location_slug == location['slug']:
                    context['selected_location_data'] = location
                    break
            else:
                raise Http404("Location does not exist.")

        context.update({
            "canonical_url": canonical_url,
        })

        return render(request, self.template_name, context)

class PetDetailView(TemplateView):
    template_name = 'pinogy_pets/pet_app_hook.html'
    
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get(self, request, pet_type_slug=None, breed_slug=None, pet_id = None, *args, **kwargs):
        
        client = PWAPI()
        pet = client.get_pet(pet_id,qp_public_call=False)
        if(pet['pbrd_slug']==breed_slug):
            pet['selected_plural_pet_type'] = pet['ptype_plurals'].get(pet['ptype_name'], pet['ptype_name'])

            # FIXME: this is hotfix only for mypuppydreams
            # if it works well then we will change this and update canonical to breed detail page
            PINOGY_ACCESS_KEY = settings.PINOGY_ACCESS_KEY
            if PINOGY_ACCESS_KEY in ["Q49PtcHw8Tz3sBSgQt7g"]:
                breed_detail_page_url = reverse('pinogy_breeds:breed_detail', kwargs={'pet_type_slug': pet_type_slug, 'breed_slug': breed_slug})
                canonical_url = f"{request.scheme}://{request.get_host()}{breed_detail_page_url}"
            else: 
                pet_breed_url = reverse('pinogy_pet:breeds_pet_type', kwargs={'pet_type_slug': pet_type_slug, 'breed_slug': breed_slug})
                canonical_url = f"{request.scheme}://{request.get_host()}{pet_breed_url}"
            
            context = {
                'selected_pet_slug': pet_id,
                'selected_pet_type_slug': pet_type_slug,
                'selected_breed_slug': breed_slug,
                'selected_pet_data':  pet,
                'pet_id': pet_id,
                'canonical_url': canonical_url,
            }
            return render(request, self.template_name, context)
        else:
            return redirect(reverse('pinogy_pet:pet_type', args=[pet_type_slug]))
        

class PetCollectionFormView(CollectionFormMixin):
    
    form_class = PetCollectionForm
    template_name = 'pinogy_pets/forms/ask_about_me.html' 


class AdoptMeView(TemplateView):
    template_name = 'pinogy_pets/adopt_me.html'

    # contact us form on sold pet page
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get(self, request, pet_type_slug=None, breed_slug=None, pet_id=None, *args, **kwargs):
        client = PWAPI()
        context = {}

        try:
            # should pass qp_public_call=False to get details for sold pets
            pet = client.get_pet(pet_id, qp_public_call=False)
            is_pet_commerce_available = pet['pet_petstatus_id'] in (utils.STATUS_AVAILABLE, utils.STATUS_COMING_SOON)
            pet["pet_image"] =  ApiPetPhoto.image_objects.get_pet_image(client, pet['pet_id'], pet['pet_image_file_ids'][0]).url() \
                                if pet['pet_has_images'] \
                                else '/static/pinogy_shop/img/default-product.png'
                    
        except django.core.exceptions.ObjectDoesNotExist:
            raise Http404('Page not found')

        if not is_pet_commerce_available or pet['pet_price'] in ['0.00', '0']:
            return HttpResponseRedirect(
                reverse(
                    'pinogy_pet_detail:pet_detail', kwargs={
                        'pet_type_slug': pet_type_slug,
                        'breed_slug': breed_slug,
                        'pet_id': pet_id,
                    })
            )

        resp = client.get_pet_addons(pet_id).get('objects', None)
            
        # add product price to product based on location
        pet_loc_id = pet['pet_loc_entity_id']
        for addon_product in resp:
            
            if addon_product["product"] is None:
                continue
            
            for product_price in addon_product["product"]["product_prices"]:
                if pet_loc_id in product_price['location_ids']:
                    addon_product['addon_product_price'] = product_price['price']
                    break
            else:
                addon_product['addon_product_price'] = '0.00'

        # Adding image to bundle,regular addon
        is_addons_with_image = False
        for addon in resp:

            if ( 
                (addon.get("variation_id") and not addon["variation"]["products"][0]["images"]) or
                (not addon.get("variation_id") and not addon["product"]["images"] and addon.get("product", {}).get("kind") == "Regular")   
            ):
                continue
            
            # update the flag if addons contains any contains with image
            if not addon.get("variation_id") and addon.get("product", {}).get("kind") == "Bundle": 
                is_addons_with_image = True
            
            # Get image object from addon product
            if addon.get("variation_id"):
                addon_product_images = addon["variation"]["products"][0]["images"]
            else:
                addon_product_images = addon["product"]["images"]
                
            if addon_product_images:
                # Display First image if product have multiple image
                addon_image = utils.get_addon_image_url(addon_product_images[0]["product_id"], addon_product_images[0]["image_id"])
            else:
                addon_image = utils.get_addon_image_url()

            addon["addon_image"] = addon_image
        
        # Create a list of all required addon
        # For variant addon adding varation id
        required_addon = []
        for addon in resp:
            if addon.get("variation_id") and addon.get("is_required"):
                required_addon.append(addon.get("variation_id"))
            elif addon.get("is_required"):
                required_addon.append(addon.get("product", {}).get("id", None))
        context["required_addon"] = required_addon
        
        pt_setting = APIPetTypeSetting()
        context["pet_setting"] = pt_setting.get_pet_type_setting_obj(pet["pet_type_id"])

        context.update({
            'selected_pet_type_slug': pet['ptype_slug'],
            'selected_breed_slug': pet['pbrd_slug'],
            'breed_id': pet['pet_breed_id'],
            'pet_id': int(pet_id),
            'pet_name': pet['pet_name'] or '',
            'is_pet_commerce_available': is_pet_commerce_available,
            'selected_pet_data': pet,
            'addons': resp,
            'pet_price': utils.get_pet_price(client, pet_id),
            'is_addons_with_image': is_addons_with_image
        })
        return render(request, self.template_name, context)