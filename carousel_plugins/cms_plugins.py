from django.urls import reverse, NoReverseMatch
from cms.models import Page
from cms.plugin_pool import plugin_pool
from cmsplugin_cascade.plugin_base import CascadePluginBase

from carousel_plugins.forms import CarouselPluginForm, GridPluginForm
from carousel_plugins.models import CarouselPluginModel, GridPluginModel
from pinogy_testimonials.models import Testimonial
from carousel_plugins.utils import (
    get_available_pets, 
    get_similar_pets,
    get_breed_available_pets,
    get_brands_data, 
    get_promotions_data,
    get_promotions_data_carousel,
    get_pet_status_list,
    get_brand_image_from_db,
    get_promotion_image_from_db
)
from pos_api.pos_client import PWAPI
from django.core.cache import cache
from pos_api.utils import add_pet_image
from pinogy_pet.pos_api import APIPetTypeSetting
from djangocms_blog.models import Post
from common_plugins.forms import AvailablePuppyCollectionForm
from common_plugins.utils import get_stores_data
import json
@plugin_pool.register_plugin
class CarouselPlugin(CascadePluginBase):
    name = "Carousel Plugin"
    module = "Pinogy"
    model = CarouselPluginModel
    form = CarouselPluginForm
    # render_template = "carousel/carousel_plugin.html"
    change_form_template = "carousel/carousel_change_form.html"
    cache = False

    def render(self, context, instance, placeholder):
        try:
            context = super().render(context, instance, placeholder)
            context['available_puppy_collection_form'] = AvailablePuppyCollectionForm
            client = PWAPI()
            request = context["request"]

            # getting current store_id
            store_data = get_stores_data(client=client)
            default_store_id = None
            if len(store_data) > 0:
                default_store_id = store_data[0].get('id',None)

            store_id = request.session.get('store_location_id') or \
                request.COOKIES.get('store_location_id') or default_store_id
            
            context['location_id'] = store_id
            context['breed'] = context.get('selected_breed_data', None)

            # Add button action link in context
            if instance.glossary.get("first_button_internallink"):
                page = Page.objects.filter(
                    id=instance.glossary.get("first_button_internallink", {}).get("pk")
                ).first()
                if page:
                    context["first_btn_link"] = page.get_absolute_url()
                elif instance.glossary.get("first_button_link"):
                    context["first_btn_link"] = instance.glossary.get("first_button_link")
            elif instance.glossary.get("first_button_link"):
                context["first_btn_link"] = instance.glossary.get("first_button_link")

            if instance.glossary.get("second_button_internallink"):
                page = Page.objects.filter(
                    id=instance.glossary.get("second_button_internallink", {}).get("pk")
                ).first()
                if page:
                    context["second_btn_link"] = page.get_absolute_url()
                elif instance.glossary.get("second_button_link"):
                    context["second_btn_link"] = instance.glossary.get("second_button_link")
            elif instance.glossary.get("second_button_link"):
                context["second_btn_link"] = instance.glossary.get("second_button_link")

            #update title 

            if instance.glossary.get('title_text') != None or instance.glossary.get('title_text') != '':
                title = instance.glossary.get('title_text')
                breed_name = context.get("selected_breed_slug", '')
                breed_name = breed_name[:-1].title() if breed_name.endswith('s') else breed_name.title()
                title = title.replace("{breed_name}",breed_name)
                title = title.replace("{pet_type}",context.get("selected_pet_type_slug", ''))
                instance.glossary['title_text'] = title


            # Add carousel items
            self.client = PWAPI()
            if instance.glossary.get("carousel_type") == "PETS":
                context["items"] = self.get_pets_for_carousel(instance=instance, context=context)
                if context["items"]:
                    pt_setting = APIPetTypeSetting()
                    context["pet_setting"] = pt_setting.get_pet_type_setting_obj(context["items"][0]["pet_type_id"])
            elif instance.glossary.get("carousel_type") == "TESTIMONIALS":
                context["items"] = self.get_testimonals_for_carousel(instance=instance)
            elif instance.glossary.get("carousel_type") == "PROMOTIONS":
                context["items"] = self.get_promotions_for_carousel(instance = instance)
            elif instance.glossary.get("carousel_type") == "BRANDS":
                context["items"] = self.get_brand_imgs_for_carousel(instance = instance)
            elif instance.glossary.get("carousel_type") == "BLOG":
                context["items"] = Post.objects.filter()    
            return context
        except Exception as e:
            return context
      

    def get_render_template(self, context, instance, placeholder):
        if instance.glossary.get("carousel_type") == "PETS":
            return instance.glossary.get("pet_layout")
        elif instance.glossary.get("carousel_type") == "TESTIMONIALS":
            return instance.glossary.get("testimonial_layout")
        elif instance.glossary.get("carousel_type") == "PROMOTIONS":
            return instance.glossary.get("promotion_layout")
        elif instance.glossary.get("carousel_type") == "BRANDS":
            return instance.glossary.get("brand_layout")
        elif instance.glossary.get("carousel_type") == "BLOG":
            return instance.glossary.get("blog_layout")

    def get_pets_for_carousel(self, instance, context):
        pet_type_names = instance.glossary.get("pet_type", [])
        location_ids = instance.glossary.get("pet_location_filter", [])
        pet_status_id = instance.glossary.get("pet_status_filter", [])
        pet_data_source = instance.glossary.get("pet_source", "DEFAULT")

        # Breed/PetType slug comes from Breed/Pet detail view
        # To display Available/Similar Puppies needs to be available in the page context
        breed_slug = context.get("selected_breed_slug")
        pet_type_slug = context.get("selected_pet_type_slug")

        # Remove 'ALL' from pet_status_id list
        # 'ALL' has been removed, some old plugins could have this in the data
        if 'ALL' in pet_status_id:
            pet_status_id.remove("ALL")

        if pet_data_source == "DEFAULT":
            pet_list = get_available_pets(
                client=self.client,
                pet_type_names=pet_type_names,
                location_ids=location_ids,
                pet_status_id=pet_status_id,
                offset=0,
                limit=12,  # limit : to get the number of elements  
            ).get("pets", [])


            if pet_list:
                pt_setting = APIPetTypeSetting() 
                pet_setting = pt_setting.get_pet_type_setting_obj(pet_list[0]["pet_type_id"])

                for pet in pet_list:
                    pet["pet_images"] = add_pet_image(
                        self.client,
                        pet.get("pet_image_file_ids"), pet.get("pet_id")
                    )

                    # Handled the pet price
                    sale_price = None
                    normal_price = None
                    disabled_price = None
                    
                    if pet_setting.sale_price_list:
                        sale_price = pet['pet_sale_price']
                        if sale_price in ['0.00', '0.0', '0'] or not sale_price:
                            sale_price = None
                            pet['pet_sale_price'] = None

                    if pet_setting.normal_price_list:
                        normal_price = pet['pet_price']
                        if normal_price in ['0.00', '0.0', '0'] or not normal_price:
                            normal_price = None
                            pet['pet_price'] = None

                        if sale_price and sale_price != normal_price:
                            disabled_price = normal_price
                    
                    pet['actual_price'] = sale_price or normal_price
                    pet['disabled_price'] = disabled_price

        elif pet_data_source == "SIMILAR_PETS" and breed_slug:
            pet_list = get_similar_pets(
                client=self.client,
                breed_slug=breed_slug,
                locations=location_ids,
                pet_type_slug=pet_type_slug 
            )
        elif pet_data_source == "AVAILABLE_PETS":
            pet_list = get_breed_available_pets(
                client=self.client,
                breed_slug=breed_slug,
                locations=location_ids,
                pet_type_slug=pet_type_slug
            )
        else:
            pet_list = []
        
        return pet_list

    def get_testimonals_for_carousel(self, instance):
        items=Testimonial.objects.filter(is_published=True)
        return items

    def get_promotions_for_carousel(self, instance):

        result = cache.get("promotion_list_carousel")

        # if result is None:

            # result = get_promotions_data(client=self.client,kind=['Astro'])   
        
        # Handle Store and Astro pomotions 
        promotionsData=[]
        promoType=[]
        if len(instance.glossary['promotions_type'])>0:
            for key in instance.glossary['promotions_type']:
                if key=='store_promotions':
                    promoType.extend(storePromotion)
                elif key=='PETZ':
                    promoType.append('PETZ')
                elif key=='astro_promotions':
                    promoType.append('Astro')
                elif key=='Astro Frequent Buyer':
                    promoType.append('Astro Frequent Buyer')
                elif key=='Astro Offer':
                    promoType.append('Astro Offer')
        else:
            promoType=["Price", "Quantity","Amount Off", "Percent Off", "Frequent Buyer","Astro","Astro Offer","PETZ","Astro Frequent Buyer"]

        promotionsData=get_promotions_data_carousel(client=self.client,kind=promoType)

        # if 'promotions_type' in instance.glossary and instance.glossary['promotions_type'] and len(instance.glossary['promotions_type']) > 0 and len(instance.glossary['promotions_type']) < 2:
        #     if instance.glossary['promotions_type'][0]=='astro_promotions':
        #         promotionsData=get_promotions_data_carousel(client=self.client,kind=['Astro'])#[x for x in result if x['is_ecommerce_astro_offer']==True]
        #     elif instance.glossary['promotions_type'][0]=='store_promotions':
        #         promotionsData=get_promotions_data_carousel(client=self.client,kind=storePromotion)#[x for x in result if  x['kind'] != 'Astro' and x['kind'] != 'PETZ']
        # #handle if no image available in promotions
        # promotionsData=[imgdata for imgdata in promotionsData if len(imgdata['images'])>0]
        
        for promotion in promotionsData:
            if isinstance(promotion['images'], list):
                promotion['images'] = get_promotion_image_from_db(
                    client=self.client, promotion_id=promotion['id'], promotion_image_id=promotion['images'][0]['id']) \
                    if promotion['images'] \
                    else get_promotion_image_from_db(client=self.client, promotion_id=promotion['id']
                )
            
            try:
                promotion["product_page_url"] = reverse('pinogy_shop:product_list_page_promotion', kwargs={'promotion_slug': promotion['slug']})
            except NoReverseMatch:
                promotion["product_page_url"] = "#"
        cache.set("promotion_list_carousel", result, 60 * 60)     
        return promotionsData
    
    def get_brand_imgs_for_carousel(self, instance):

        result = cache.get("brand_list_carousel")

        if result is None:

            result = get_brands_data(client=self.client)   
            for brand in result:
                brand['images'] = get_brand_image_from_db(
                    client=self.client, brand_id=brand['id'], brand_image_id=brand['images'][0]['id']) if brand['images'] else get_brand_image_from_db(client=self.client, brand_id=brand['id']
                )
                try:
                    brand["product_page_url"] = reverse('pinogy_shop:brand_wise_product_list_page', kwargs={'brand' : brand['slug']})
                except NoReverseMatch:
                    brand["product_page_url"] = "#"

            cache.set("brand_list_carousel", result, 60 * 60 * 24 * 7)
            
        return result
    
# const value for pomotion
storePromotion = ["Price", "Quantity","Amount Off", "Percent Off", "Frequent Buyer"]

@plugin_pool.register_plugin
class GridPlugin(CascadePluginBase):
    name = "Grid plugin"
    module = "Pinogy"
    model = GridPluginModel
    form = GridPluginForm
    render_template = "grid/grid_page_base.html"
    change_form_template = "grid/grid_plugin_template.html"
    cache = False

    def render(self, context, instance, placeholder):
        self.client = PWAPI()
        ''' fetch all common data to show'''
        title = instance.glossary.get('title_text')
        gridName = instance.glossary.get('gridName')
        context['instance'] = instance
        
        if instance.glossary.get("grid_type") == "PETS" :
            pet_list = self.get_pets_for_carousel(instance=instance, context=context)
            context['pet_type_data'] = pet_list
            return context
        
        elif instance.glossary.get("grid_type") == "BRANDS":
            context["pet_type_data"] = self.get_brand_imgs_for_carousel(instance = instance)
            return context
        
        elif instance.glossary.get("grid_type") == "PROMOTIONS":
            context["pet_type_data"] = self.get_promotions_for_carousel(instance = instance)
            return context
        
        elif instance.glossary.get("grid_type") == "TESTIMONIALS":
            context["pet_type_data"] = self.get_testimonals_for_carousel(instance = instance)
            return context
        
        elif instance.glossary.get("grid_type") == "BLOG":
            context["pet_type_data"] = Post.objects.filter() 
            return context
     
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        
        return super().render_change_form(request, context, add, change, form_url, obj)
    
    def save_model(self, request, obj, form, change):
        if obj is not None:
            obj.grid_button_data = json.loads(obj.grid_button_data)
            obj.save()
        super().save_model(request, obj, form, change)

    def get_pets_for_carousel(self, instance, context):

        # THESE FILTERS ARE APPLIED FROM PLUGIN
        filters = {}
        if 'Breed' in instance.glossary.get('pet_filter', []):
            breed_slug = instance.grid_breeds_list or []
            filters['qp_pbrd_display_name'] = json.loads(breed_slug)

        if "Sex" in instance.glossary.get('pet_filter', []):
            filters['qp_pet_gender'] = instance.glossary.get('grid_pet_sex', [])

        if "on_sale" in instance.glossary.get('pet_filter', []):
            filters['qp_pet_is_on_sale']  = instance.glossary.get('grid_Is_pet_on_sale', 'false')

        pet_type_names = instance.glossary.get("grid_pet_type", [])
        location_ids = instance.glossary.get("grid_pet_location", [])
        pet_status_id = instance.glossary.get("grid_pet_status", [])
        pet_data_source = instance.glossary.get("pet_source", "DEFAULT")

        if pet_data_source == "DEFAULT":
            pet_list = get_available_pets(
                client=self.client,
                pet_type_names=pet_type_names,
                location_ids=location_ids,
                pet_status_id=pet_status_id,
                filters=filters,
                offset=0,
                limit=12,  # limit : to get the number of elements  
            ).get("pets", [])


            if pet_list:
                pt_setting = APIPetTypeSetting() 
                pet_setting = pt_setting.get_pet_type_setting_obj(pet_list[0]["pet_type_id"])

                for pet in pet_list:
                    pet["pet_images"] = add_pet_image(
                        self.client,
                        pet.get("pet_image_file_ids"), pet.get("pet_id")
                    )

                    # Handled the pet price
                    sale_price = None
                    normal_price = None
                    disabled_price = None
                    
                    if pet_setting.sale_price_list:
                        sale_price = pet['pet_sale_price']
                        if sale_price in ['0.00', '0.0', '0'] or not sale_price:
                            sale_price = None
                            pet['pet_sale_price'] = None

                    if pet_setting.normal_price_list:
                        normal_price = pet['pet_price']
                        if normal_price in ['0.00', '0.0', '0'] or not normal_price:
                            normal_price = None
                            pet['pet_price'] = None

                        if sale_price and sale_price != normal_price:
                            disabled_price = normal_price
                    
                    pet['actual_price'] = sale_price or normal_price
                    pet['disabled_price'] = disabled_price

        else:
            pet_list = []
        
        return pet_list

    def get_brand_imgs_for_carousel(self, instance):

        result = cache.get("brand_list_carousel")

        if result is None:

            result = get_brands_data(client=self.client)   
            for brand in result:
                brand['images'] = get_brand_image_from_db(
                    client=self.client, brand_id=brand['id'], brand_image_id=brand['images'][0]['id']) if brand['images'] else get_brand_image_from_db(client=self.client, brand_id=brand['id']
                )
                try:
                    brand["product_page_url"] = reverse('pinogy_shop:brand_wise_product_list_page', kwargs={'brand' : brand['slug']})
                except NoReverseMatch:
                    brand["product_page_url"] = "#"

            cache.set("brand_list_carousel", result, 60 * 60 * 24 * 7)
            
        return result
        
    def get_promotions_for_carousel(self, instance):

        result = cache.get("promotion_list_carousel")

        # if result is None:

            # result = get_promotions_data(client=self.client,kind=['Astro'])   
        
        # Handle Store and Astro pomotions 
        promotionsData=[]
        promoType=[]
        # if len(promoType)>0: # give the promotion type here from frontend
        if instance.glossary['promotion_type']: # give the promotion type here from frontend
            # for key in instance.glossary['promotions_type']:
            key = instance.glossary['promotion_type']
            if key=='store_promotions':
                promoType.extend(storePromotion)
            elif key=='PETZ':
                promoType.append('PETZ')
            elif key=='astro_promotions':
                promoType.append('Astro')
            elif key=='Astro Frequent Buyer':
                promoType.append('Astro Frequent Buyer')
            elif key=='Astro Offer':
                promoType.append('Astro Offer')
        else:
            promoType=["Price", "Quantity","Amount Off", "Percent Off", "Frequent Buyer","Astro","Astro Offer","PETZ","Astro Frequent Buyer"]

        promotionsData=get_promotions_data_carousel(client=self.client,kind=promoType)

        # if 'promotions_type' in instance.glossary and instance.glossary['promotions_type'] and len(instance.glossary['promotions_type']) > 0 and len(instance.glossary['promotions_type']) < 2:
        #     if instance.glossary['promotions_type'][0]=='astro_promotions':
        #         promotionsData=get_promotions_data_carousel(client=self.client,kind=['Astro'])#[x for x in result if x['is_ecommerce_astro_offer']==True]
        #     elif instance.glossary['promotions_type'][0]=='store_promotions':
        #         promotionsData=get_promotions_data_carousel(client=self.client,kind=storePromotion)#[x for x in result if  x['kind'] != 'Astro' and x['kind'] != 'PETZ']
        # #handle if no image available in promotions
        # promotionsData=[imgdata for imgdata in promotionsData if len(imgdata['images'])>0]
        
        for promotion in promotionsData:
            if isinstance(promotion['images'], list):
                promotion['images'] = get_promotion_image_from_db(
                    client=self.client, promotion_id=promotion['id'], promotion_image_id=promotion['images'][0]['id']) \
                    if promotion['images'] \
                    else get_promotion_image_from_db(client=self.client, promotion_id=promotion['id']
                )
            
            try:
                promotion["product_page_url"] = reverse('pinogy_shop:product_list_page_promotion', kwargs={'promotion_slug': promotion['slug']})
            except NoReverseMatch:
                promotion["product_page_url"] = "#"
        cache.set("promotion_list_carousel", result, 60 * 60)     
        return promotionsData
    
    def get_testimonals_for_carousel(self, instance):
        items=Testimonial.objects.filter(is_published=True)
        return items
