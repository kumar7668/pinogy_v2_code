import re
import json

from typing import Optional, Union, List
from cms.plugin_pool import plugin_pool
from cmsplugin_cascade.plugin_base import CascadePluginBase
from django.utils.translation import gettext_lazy as _
from django.http import Http404
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.templatetags.static import static
from cmsplugin_cascade.models import CascadeElement
from django.urls import path
from django.conf import settings
from urllib.parse import quote
from common_plugins import utils
from cms.models import Page
from .models import ApiPetAdCard
from common_plugins.forms import CollectionForm, SchedulePlaydate,OtpVerificationForm,CustomerVerificationForm
from custom_design.models import ThemeConfiguration
from pinogy_breeds.pos_api import BreedDetail
from pos_api.models.pet import ApiPetPhoto
from carousel_plugins.utils import (
    get_available_pets,
)
from common_plugins import utils
from pos_api.utils import add_pet_image
from pos_api.pos_client import PWAPI
from pinogy_pet.models import ApiPetBadgePhoto
from pinogy_pet.forms import PetTypeListPluginForm, PetListPluginForm, PetDetailPluginForm, PetPurchaseForm, PetCollectionForm
from pinogy_pet.pos_api import PetTypeList, APIPetTypeSetting, PetTypeSetting
from pinogy_pet.utils import ( 
    get_photos_meta, get_videos_meta, get_pet_filters, get_addon_image_url, get_play_date_schedule,
    STATUS_AVAILABLE, STATUS_COMING_SOON,
)
from .models import (
    PetDetailPluginModel, PetListPluginModel
)
ad_card_index = 0
class PetImagesMixin:
    
    def _get_pet_images(self, client, pet_id):
        cache_key = f"PetImagesMixin:_get_pet_images:{pet_id}"
        cache_time_out = 60 * 60 * 24
        
        result = cache.get(cache_key)
        if result:
            return result
        
        photos_meta = get_photos_meta(client, pet_id)
        
        pet_images = ApiPetPhoto.objects.get_images(
            client = client, 
            api_images_data = photos_meta, 
            model_defaults = {'is_badges': False},  # model_defaults
            model_filters = {'pet_id': pet_id, 'is_badges': False},  # model_filters
            non_defaults = {'pet_id': pet_id}  # non_defaults
        )
        # commented by mark to see if these are the images in redis
        # cache.set(cache_key, pet_images, cache_time_out)
        return pet_images

    def _get_pet_badges(self, client, pet_id, badges_data):
        cache_key = f"PetImagesMixin:_get_pet_badges:{pet_id}"
        cache_time_out = 60 * 60 * 24
        
        result = cache.get(cache_key)
        if result:
            return result
        
        if not badges_data:
            return []

        pet_badges_data = ApiPetBadgePhoto.objects.get_pet_badges(client, badges_data)
        
        cache.set(cache_key, pet_badges_data, cache_time_out)
        return pet_badges_data
    
class PetVideosMixin:
     
     def _get_pet_videos(self, client, pet_id):
        cache_key = f"PetVideosMixin:_get_pet_videos:{pet_id}"
        cache_time_out = 60 * 60 * 24
        
        result = cache.get(cache_key)
        if result:
            return result
        
        videos_meta = get_videos_meta(client, pet_id)

        pet_videos_data = videos_meta

        cache.set(cache_key, pet_videos_data, cache_time_out)
        return pet_videos_data


@plugin_pool.register_plugin
class PetTypeListPlugin(CascadePluginBase):
    """
    Plugin to display all available pet types
    """

    name = "Pet Types List"
    module = "Pinogy"
    form = PetTypeListPluginForm
    change_form_template = "custom_design/admin/change_form.html"
    render_template = "plugins/pet_type_list.html"
    cache = False
    
    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['collection_form'] = CollectionForm

        request = context["request"]
        
        store_id = request.session.get('store_location_id') or \
            request.COOKIES.get('store_location_id')
        
        context['shopwindow_enable'] = utils.is_shopwindow_enable(store_id)
        # pet_type = instance.glossary.get("pet_types_list")
        pet_types_obj = PetTypeList()
        
        # If pet type is not available in context than only fetch from POS
        # Passing context from here - pinogy_pet/views.py
        # pet_types_list = context.get('pet_types_list')        
        # if not pet_types_list:
        if instance.glossary.get("pet_types_list"):
            pet_types_list = pet_types_obj.get_pet_type_list(instance.glossary['pet_types_list'])
        else:
            pet_types_list = pet_types_obj.get_pet_type_list(None)
        
        temp=pet_types_list
        for dataList in temp:
            res= pet_types_obj.get_pet_type_photo(dataList.id, dataList.name)
            if res is not None:
                dataList.image_url=res.url
            else:
                dataList.image_url = "/static/images/dog-placeholder-img.webp"
        context['pet_list'] = pet_types_list
        return context


@plugin_pool.register_plugin
class PetListPlugin(CascadePluginBase, PetImagesMixin):
    """
    Plugin to display Pet List of all available pet types
    """
    name = "Pet List"
    module = "Pinogy"
    form = PetListPluginForm
    model = PetListPluginModel
    change_form_template = "form/pet_list.html"
    render_template = "plugins/flow.html"
    cache = False

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        pet_list_setting = cache.get("pet_list_settings")

        # Define the detailed pet info to display
        pet_info = [
            ('petid', 'Pet ID', False),
            ('petname', 'Name', False),
            ('sex', 'Sex', False),
            ('birthdate', 'Birth Date', False),
            ('usda', 'USDA Number', False),
        ]

        # Filter the detailed pet info based on pet settings
        filtered_pet_info = []
        for atr in pet_info:
            attr_name, attr_value = atr[0], atr[1]
            if getattr(pet_list_setting, attr_name).visible:
                is_visible = True
            else:
                is_visible = False
            
            filtered_pet_info.append((attr_name, attr_value, is_visible))
        
        context['filtered_pet_info'] = filtered_pet_info
        
        return super().render_change_form(request, context, add, change, form_url, obj)

    
    def get_pet_filters(self, client: Optional[PWAPI] = None, pet_type_name: Optional[str] = None, pet_loc_entity_id: Optional[List[str]] = None):
        cache_key = f'available_pets_filters:{pet_type_name}:{pet_loc_entity_id}'
        result = cache.get(cache_key)
        if result:
            return result

        api_pet_list_filters = get_pet_filters(client=client, pet_type_name=pet_type_name, pet_loc_entity_id=pet_loc_entity_id)

        pet_list_filters = {'filter_values': {}, 'filters':[]}
        for k,v in api_pet_list_filters.get('filter_values').items():
            if v and isinstance(v, dict) and len(v) > 1:
                pet_list_filters['filter_values']['qp_'+k] = dict(sorted(v.items()))

        for filter in api_pet_list_filters.get('filters'):
            if pet_list_filters.get('filter_values').get(filter.get('param')) and filter.get('enabled'):
                # changed filter sub status name to status 
                if filter['param'] == 'qp_psubstatus_name':
                    filter['name'] = 'Status'
                pet_list_filters.get('filters').append(filter)
            elif pet_list_filters.get('filter_values').get(filter.get('param')):
                pet_list_filters.get('filter_values').pop(filter.get('param'))
        
        cache.set(cache_key, pet_list_filters, 3600)

        return pet_list_filters
    
    def get_render_template(self, context, instance, placeholder):
        return instance.glossary.get("template_type") or "plugins/flow.html"
    
    def get_plugin_urls(self):
        return [
            path('filters/<int:instance_id>/', pet_list_ajax, name='pet_list_filters'),
            path('ajax/page/<int:instance_id>/', pet_list_ajax, name='pet_list_page'),
        ]
    
    def render(self, context, instance, placeholder):
        
        context = super().render(context, instance, placeholder)
        
        client = PWAPI()
        request = context['request']
        context['pet_collection_form'] = PetCollectionForm
        context['collection_form'] = CollectionForm
        request = context["request"]
        client = PWAPI()
        store_data = utils.get_stores_data(client=client)
        default_store_id = None
        if len(store_data) > 0:
            default_store_id = store_data[0].get('id',None)

        store_id = request.session.get('store_location_id') or \
            request.COOKIES.get('store_location_id') or default_store_id
        
        shopwindow_location_ids = utils.get_shopwindow_location_ids()

        context['is_enable']=  store_id in shopwindow_location_ids
        context['playdate_form'] = SchedulePlaydate
        # Page related
        offset = 0
        limit = 17
        next_page_available = True
        page = 1
        
        breed_slug = context.get('selected_breed_data', {}).get('slug') or context.get('selected_breed_slug') 

        pet_type_ = context.get('selected_pet_type_slug')
        pet_types_obj = PetTypeList()
        if pet_type_ is None:
            pet_type = instance.glossary.get("breeds_pet_type")
            pet_types_list = pet_types_obj.get_pet_type_list(pet_type)
            pet_type_names=[o.name for o in pet_types_list]
        else:
            pet_type_names=[o.name for o in pet_types_obj.get_pet_type_list(None) if o.slug==pet_type_]

        # Get location and status ids from plugin setting 
        pet_status_id = instance.glossary.get("pet_status_filter", [])
        locations_list = instance.glossary.get("pet_location_filter", [])

        # Get the location data from page context or ajax request  
        # if loctaion id is available than override the location list to only one sepcific location
        location_id = context.get('selected_location_data', {}).get('id') or context.get('selected_location_id')
        if location_id:
            locations_list = [location_id]

        # Get Filters from request
        filters = {}
        if "filters" in request.path or "ajax/page" in request.path:
            filters = json.loads(request.body)
        else:
            # filter_val=self.get_pet_filters(client=client, pet_type_name=pet_type_names[0])
            # filter_val['filters']=[x for x in filter_val['filters'] if x['param'] in instance.glossary.get('pet_filter')]
            context["filters"] = self.get_pet_filters(client=client, pet_type_name=pet_type_names[0], pet_loc_entity_id=locations_list)
        
        if request.GET.get('page'):
            page = int(request.GET.get('page'))
            offset = ((page-1) * limit) - 1
        else:
            global ad_card_index
            ad_card_index = 0
            limit = 16

        api_pet_result = get_available_pets(
            client=client,
            pet_type_names=pet_type_names,
            breed_slugs=breed_slug,
            location_ids=locations_list,
            pet_status_id=pet_status_id,
            order_by="pbrd_display_name, pet_has_images DESC, pet_age DESC, pet_id",
            pet_with_images=False,
            filters=filters,
            offset=offset,
            limit=limit,
        )
        if len(api_pet_result['pets'])>0:
            pet_list = api_pet_result.get("pets", [])
        else:
            pet_list=[]
        if api_pet_result.get("total") is not None:
            total_pet = int(api_pet_result.get("total", '0'))
        else:
            total_pet=0
        if (page * limit) >= total_pet:
            next_page_available = False

        pet_setting = PetTypeSetting()
        if pet_list:
            pt_setting = APIPetTypeSetting()
            pet_setting = pt_setting.get_pet_type_setting_obj(pet_list[0]["pet_type_id"])
        
        # caching the data for passing in the pet list editing component
        cache.set("pet_list_settings", pet_setting, 60*60*24*7)


        schedule_a_play_date = False # check wheater the schedule a play date is enabled from plugin or not
        for key, value in instance.button_data.items():
            if value.get("button_selector") == "schedule_a_playdate":
                schedule_a_play_date = True 
        for pet in pet_list:
            pet["pet_images"] = add_pet_image(
                client,
                pet.get("pet_image_file_ids"), pet.get("pet_id")
            )
            
            pet['pet_badges_data'] = self._get_pet_badges(client, pet.get("pet_id"), pet['pet_badges'])

            pet["is_male"]=pet['pet_gender']=='Male'

            # get schedule date
            client = PWAPI()
            pet['selected_store'] = utils.get_selected_store(client=client, store_id=pet['pet_currently_at_entity_id'])
            pet['current_pet_box_visits_schedule'] = get_play_date_schedule(client, pet).items()

            pet["shopwindow_enable"]=False

            if pet['pet_loc_entity_id'] in shopwindow_location_ids:
                pet["shopwindow_enable"]=True

            phone_number = None
            contact_numbers =pet.get('loc_contact_numbers')
            if contact_numbers:
                if 'Office' in contact_numbers:
                    phone_number = contact_numbers.get('Office')
                    pet['phone_number']=phone_number
                else:
                    if 'Mobile' in contact_numbers:
                        phone_number = contact_numbers.get('Mobile')
                        pet['phone_number']=phone_number

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

            if schedule_a_play_date and pet['current_pet_box_visits_schedule']:
                pet['show_play_date'] = True
            else:
                pet['show_play_date'] = False

        
        ad_cards = ApiPetAdCard.get_ad_cards_from_db(pet_type_id=pet_setting.pet_type_id)
        if ad_cards:
                for i, pet_obj in enumerate(pet_list):
                    if (i + 1) % 4 == 0:  
                        if ad_cards[ad_card_index]['url'] == None:
                            continue
                        
                        pet_obj['ad_card'] = True
                        pet_obj['ad_card_img'] = ad_cards[ad_card_index]['url']
                        pet_obj['ad_card_link'] = ad_cards[ad_card_index]['ad_card_link']
                        pet_obj['is_video'] = ad_cards[ad_card_index]['is_video']
                        
                        ad_card_index += 1
                        if ad_card_index == len(ad_cards):
                            ad_card_index = 0
        
        context['pet_list'] = pet_list
        context["pet_setting"] = pet_setting or {}
        context["next_page_available"] = next_page_available
        context["page"] = page + 1
        context['more_info'] = instance.glossary.get('more_info')
        context['ask_about_me'] = instance.glossary.get('ask_about_me')
        context['call_now'] = instance.glossary.get('call_now')
        context['store_id'] = store_id
        context['CustomerVerificationForm']=CustomerVerificationForm
        context['CustomerOTPVerificationForm']=OtpVerificationForm
        
        return context

        
@plugin_pool.register_plugin
class PetDetailPlugin(CascadePluginBase, PetImagesMixin, PetVideosMixin,):
    """
    Plugin to display Pet List of all available pet types
    """
    name = "Pet Details"
    module = "Pinogy"
    form = PetDetailPluginForm
    model = PetDetailPluginModel
    change_form_template = "form/pet_detail.html"
    render_template = "plugins/pet_detail/base.html"
    allow_children = True
    alien_child_classes = True
    cache = False

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        client = PWAPI()
        
        # Extract the pet ID from the URL parameter 'cms_path'
        path = request.GET.get('cms_path', "")
        if '?edit' not in path:
            pet_id = path.strip('/').split('/')[-1]
        else:
            pet_id = path.strip('/').split('/')[-2]

        
        # Fetch pet data from the API
        pet_data = client.get_pet(pet_id, qp_public_call=False)
        
        pt_setting = APIPetTypeSetting()
        pet_setting = pt_setting.get_pet_type_setting_obj(pet_data["pet_type_id"])

        # Getting breed data form the Api
        breed_obj = BreedDetail()
        breed_detail = breed_obj.get_breed_data(breed_slug=pet_data['pbrd_slug'])
        pet_data['breed_detail'] = breed_detail

        # Define the info types to display
        info_type = [
            ('petname', 'Name', False),
            ('normal_price_list', 'Price', False),
            ('status', 'Status', False),
            ('sex', 'Sex', False),
            ('badges', 'Badges', False)
        ]
        
        # Define the detailed pet info to display
        about_pet_info = [
            ('petid', 'ID', False),
            ('sex', 'Sex', False),
            ('birthdate', 'Birth Date', False),
            ('storecitystate', 'Store, City, State', False),
            ('storephone', 'Store Phone', False),
            ('usda', 'USDA#', False),
            ('aphis', 'USDA/APHIS Search Portal', False),
            ('breedername', 'Breeder Name', False),
            ('breedercitystate', 'Breeder City, State', False),
            ('petmarketingtext', 'Marketing Text', False)
        ]
        
        # Filter the info types based on pet settings and pet data
        filtered_info_type = []
        for atr in info_type:
            attr_name, attr_value = atr[0], atr[1]
            if attr_value == 'Price' and getattr(pet_setting, attr_name):
                is_visible = True
            elif attr_value == 'Status' and 'sub_pstatus_name' in pet_data and pet_data['sub_pstatus_name']:
                is_visible = True
            elif attr_value == 'Badges' and 'pet_badges' in pet_data and pet_data['pet_badges']:
                is_visible = True
            elif hasattr(pet_setting, attr_name) and getattr(pet_setting, attr_name).visible_detail_only:
                is_visible = True
            else:
                is_visible = False
            
            filtered_info_type.append((attr_name, attr_value, is_visible))
        
        # Filter the detailed pet info based on pet settings
        filtered_about_pet = []
        for atr in about_pet_info:
            attr_name, attr_value = atr[0], atr[1]
            if getattr(pet_setting, attr_name).visible_detail_only:
                is_visible = True
            else:
                is_visible = False
            
            filtered_about_pet.append((attr_name, attr_value, is_visible))
        
        # Filter the detailed breed info based on pos settings
        filtered_breed_info = []
        if breed_detail.notes:
            filtered_breed_info.append(('Characteristics', True))
            filtered_breed_info.append(('Description', True))
        else:
            filtered_breed_info.append(('Characteristics', False))
            filtered_breed_info.append(('Description', False))
        
        if breed_detail.metrics:
            filtered_breed_info.append(('Traits', True))
        else:
            filtered_breed_info.append(('Traits', False))
        
       
        context['filtered_info_type'] = filtered_info_type
        context['filtered_about_pet'] = filtered_about_pet
        context['filtered_breed_info'] = filtered_breed_info
        return super().render_change_form(request, context, add, change, form_url, obj)

    
    def render(self, context, instance, placeholder):
        client = PWAPI()
        context = super().render(context, instance, placeholder)
        context['playdate_form'] = SchedulePlaydate
        pet = context.get("selected_pet_data")
        context['pet_data'] = None
        if pet:
            location_id = pet['pet_loc_entity_id']
            if instance.glossary.get("custom_button_internallink"):
                page = Page.objects.filter(
                    id=instance.glossary.get("custom_button_internallink", {}).get("pk")
                ).first()
                if page:
                    context["custom_btn_link"] = page.get_absolute_url()
                elif instance.glossary.get("custom_button_link"):
                    context["custom_btn_link"] = instance.glossary.get("custom_button_link")
            elif instance.glossary.get("custom_button_link"):
                context["custom_btn_link"] = instance.glossary.get("custom_button_link")

            videos_data = self._get_pet_videos(client,pet.get("pet_id"))
            pet_videos_thumbnail=[]
            for videos in videos_data:
                videos_meta = videos.get('video',{}).get('meta', {}).get('vimeo', {}).get('pictures', {})
                base_link = videos_meta.get('base_link', None)
                if base_link is not None:
                    pet_videos_thumbnail.append(base_link)
                else:
                    pet_videos_thumbnail.append(static('pinogy_shop/img/default-product.png')) 

            pet_videos_iframe = []
            for pet_videos in videos_data:
                video_iframe = pet_videos.get('video', {}).get('embed_html', {})
                pet_videos_iframe.append(video_iframe)

            pet["pet_images"] = self._get_pet_images(client, pet.get("pet_id"))
            pet["pet_videos"] = pet_videos_iframe
            pet["pet_videos_thumbnail"] = pet_videos_thumbnail
            pet["pet_badges_data"] = self._get_pet_badges(client, pet.get("pet_id"), pet['pet_badges'])
            pet['selected_store'] = utils.get_selected_store(client=client, store_id=pet['pet_currently_at_entity_id'])

            breed_obj = BreedDetail()
            breed_detail = breed_obj.get_breed_data(breed_slug=pet['pbrd_slug'])
            pet["is_male"]=pet['pet_gender']=='Male'
            pet['breed_detail']=breed_detail
            pet['isShowList']=pet['ptype_name']=='Puppy'
            phone_number = None
            contact_numbers =pet.get('loc_contact_numbers')
            if contact_numbers:
                if 'Office' in contact_numbers:
                    phone_number = contact_numbers.get('Office')
                    pet['phone_number']=re.sub("[^0-9]", "", phone_number)
                    pet['display_phone_number']=phone_number
                else:
                    if 'Mobile' in contact_numbers:
                        phone_number = contact_numbers.get('Mobile')
                        pet['phone_number']=re.sub("[^0-9]", "", phone_number)
                        pet['display_phone_number']=phone_number
            
            pt_setting = APIPetTypeSetting()
            pet_setting = pt_setting.get_pet_type_setting_obj(pet["pet_type_id"])
            
            # Handled the pet price
            sale_price = None
            normal_price = None
            disabled_price = None

            # Adding pet price for addon
            pet["addon_pet_price"] = (
                pet["pet_sale_price"] 
                if pet["pet_sale_price"] and pet["pet_sale_price"] not in ['0.00', '0.0', '0']
                else pet["pet_price"]
            )
            
            if pet_setting.sale_price_detail:
                sale_price = pet['pet_sale_price']
                if sale_price in ['0.00', '0.0', '0'] or not sale_price:
                    sale_price = None
                    pet['pet_sale_price'] = None
                    pet_setting.sale_price_detail = False

            if pet_setting.normal_price_detail:
                normal_price = pet['pet_price']
                if normal_price in ['0.00', '0.0', '0'] or not normal_price:
                    normal_price = None
                    pet['pet_price'] = None
                    pet_setting.normal_price_detail = False

                if pet_setting.sale_price_detail and sale_price != normal_price:
                    disabled_price = normal_price

            breed_data = pet.get('breed_detail')
            if breed_data:
                # Each metric value is divided by 2 to fit into five blocks
                # The quotient (quo) will determine the number of full blocks
                # The remainder (rem) will determine if there's a half block (50% progress bar)
                # rem_val will determine the number of empty blocks (0% progress bar)
                metrics_info = []
                for metrics in breed_data.metrics:
                    val = metrics.value
                    quo = int(val/2)
                    rem = int(val%2)
                    rem_val = 5-(quo+rem)
                    metrics_info.append((list(range(quo)),list(range(rem)),list(range(rem_val)),metrics.name))
            
            pet['actual_price'] = sale_price or normal_price
            pet['disabled_price'] = disabled_price

            context['breed_metrics_info'] = metrics_info
            context['location_id'] = location_id
            context['pet_data'] = pet
            context['pet_setting'] = pet_setting
            context['current_pet_box_visits_schedule']= get_play_date_schedule(client, pet).items()
            context['collection_form'] = CollectionForm
            context['CustomerVerificationForm']=CustomerVerificationForm
            context['CustomerOTPVerificationForm']=OtpVerificationForm
            context['shopwindow_enable'] = utils.is_shopwindow_enable(location_id) # passing pet location id

            if 'pet_marketing_notes' in context['pet_data'] and context['pet_data']['pet_marketing_notes']:
                #/n not support in current Version  
                context['pet_data']['pet_marketing_notes']=context['pet_data']['pet_marketing_notes'].replace('\n', '</br>')
            
            top_btn_data = {}
            btn_data = {}
            if instance.button_data:
               btn_data = instance.button_data
               is_top = instance.button_data.get('btn1').get('button_top')
               if is_top == 'true':
                    top_btn_data = instance.button_data.get('btn1')
                    del btn_data['btn1']

            context['top_btn_data'] = top_btn_data
            context['btn_data'] = btn_data

             # Replaced the placeholder '{breed_name}' in the message with the actual breed name
            message = instance.glossary.get('message',"")

            if message is not None and message != '':
                breed_name = pet.get('pbrd_display_name') if pet.get('pbrd_display_name') else ""
                if breed_name is not None and breed_name != "":
                   breed_name = breed_name[:-1].title() if breed_name.endswith('s') else breed_name.title()
                message = message.replace("{breed_name}", breed_name)
                instance.glossary['message'] = message
            
            if message is not None and message != '':
                pet_name = pet.get('pet_name') if pet.get('pet_name') else ""
                if pet_name is not None and pet_name != "":
                   pet_name = pet_name[:-1].title() if pet_name.endswith('s') else pet_name.title()
                message = message.replace("{pet_name}", pet_name)
                instance.glossary['message'] = message

        return context
    

@csrf_exempt
def pet_list_ajax(request, instance_id):
    context = {
        "request": request,
        "selected_pet_type_slug": request.GET.get("pet_type_slug"),
        "selected_breed_slug": request.GET.get("breed_slug"),
        "selected_location_id": request.GET.get("location_id"),
    }
    plugin = PetListPlugin()
    instance = PetListPluginModel.objects.get(pk=instance_id)
    context = plugin.render(context, instance, instance.placeholder)
    template = plugin.get_render_template(context, instance, instance.placeholder)
    response = render_to_string(template, context, request=request)
    return HttpResponse(response)

@plugin_pool.register_plugin
class PetPurchasePlugin(CascadePluginBase, PetImagesMixin):
    """
    Plugin to purchase pet
    """
    name = "Pet Purchase"
    module = "Pinogy"
    form = PetPurchaseForm
    parent_classes = ["PetDetailPlugin"]
    change_form_template = "custom_design/admin/change_form.html"
    render_template = "pinogy_pets/plugins/pet_purchase.html"
    cache = False
    frame_origin = settings.CARDCONNECT_SERVER_URL

    def get_frame_source(self):
        theme_obj = ThemeConfiguration.objects.get()
        encoded_theme_attributes = {
            'primary_color': quote(theme_obj.primary_color[:-2]),
            'heading_font': quote(theme_obj.heading_font),
        }

        frame_source = (
            "/itoke/ajax-tokenizer.html?scrolling=no&tokenpropname=pinogytoken"
            "&invalidcreditcardevent=true&invalidcvvevent=true&invalidexpiryevent=true"
            "&useexpiry=true&usecvv=true&cardinputmaxlength=16"
            f"&css=input%2C%20select%7B%0A%20%20%20%20padding%3A%206px%2012px%3B%0A%20%20%20%20border%3A%201px%20solid%20{encoded_theme_attributes['primary_color']}%3B%0A%20%20%20%20border-radius%3A%200px%3B%0A%20%20%20%20outline%3A%20none%3B%0A%20%20%20%20margin-bottom%3A%2015px%3B%0A%20%20%20%20font-size%3A%2015px%3B%0A%20%20%20%20height%3A%2025px%3B%0A%20%20%20%20background-color%3A%20white%3B%0A%20%20%20%20"
            f"color%3A%20{encoded_theme_attributes['primary_color']}%3B%0A%7D%0Aselect%7B%0A%20%20%20%20width%3A%20100px%3B%0A%20%20%20%20height%3A%2040px%3B%0A%7D%0Abody%7B%0A%20%20%20%20margin%3A0%3B%0A%7D%0Alabel%7B%0A%20%20%20%20"
            f"font-family%3A%20{encoded_theme_attributes['heading_font']}%3B%0A%20%20%20%20"
            f"color%3A%20{encoded_theme_attributes['primary_color']}%3B%0A%20%20%20%20font-size%3A%2016px%3B%0A%20%20%20%20font-style%3A%20normal%3B%0A%20%20%20%20font-weight%3A%20400%3B%0A%20%20%20%20line-height%3A%20140%25%3B%0A%7D%0Abutton%3Afocus%2Cinput%3Afocus%2Ca%3Afocus%2Cselect%3Afocus%7B%0A%20%20%20%20outline%3A%20none%20!important%0A%7D"
        )

        return frame_source

    def get_pet_addons(self, client: PWAPI, pet_id: Union[int, str], pet_loc_id: Union[int, str]):
        # TODO: Add Cache
        resp = client.get_pet_addons(pet_id).get('objects', None)
            
        # add product price to product based on pet store location
        for addon_product in resp:
            
            if addon_product["variation"]:
                # Adding price for variation products
                for variation_product in addon_product["variation"]["products"]:
                    for product_price in variation_product["product_prices"]:
                        if pet_loc_id in product_price['location_ids']:
                            variation_product['addon_product_price'] = product_price['price']
                            break
                    else:
                        variation_product['addon_product_price'] = '0.00'
            else:
                # Adding price for non variant product
                for product_price in addon_product["product"]["product_prices"]:
                    if pet_loc_id in product_price['location_ids']:
                        addon_product['addon_product_price'] = product_price['price']
                        break
                else:
                    addon_product['addon_product_price'] = '0.00'

        # Adding image to bundle,regular addon
        for addon in resp:

            if ( 
                (addon.get("variation_id") and not addon["variation"]["products"][0]["images"]) or
                (not addon.get("variation_id") and not addon["product"]["images"] and addon.get("product", {}).get("kind") == "Regular")   
            ):
                continue
            
            # Get image object from addon product
            if addon.get("variation_id"):
                addon_product_images = addon["variation"]["products"][0]["images"]
            else:
                addon_product_images = addon["product"]["images"]
                
            if addon_product_images:
                # Display First image if product have multiple image
                addon_image = get_addon_image_url(addon_product_images[0]["product_id"], addon_product_images[0]["image_id"])

                addon["addon_image"] = addon_image

        resp = sorted(resp, key=lambda x: not x['is_required'])

        return resp

    def get_required_addons(self, addons):
        # TODO: Add Cache
        # Addons response should be same as /api/pet_addons
        # Create a list of all required addon
        # Note: For variant addon adding varation id
        required_addon = []
        for addon in addons:
            if addon.get("variation_id") and addon.get("is_required"):
                required_addon.append(addon.get("variation_id"))
            elif addon.get("is_required"):
                required_addon.append(addon.get("product", {}).get("id", None))
        
        return required_addon
    
    def is_pet_commerce_available(self,pet_data):
        # Get pet settings from pet type settings
        pet_setting_obj = APIPetTypeSetting()
        pet_setting = pet_setting_obj.get_pet_type_setting_obj(pet_data.get('pet_type_id'))

        #check availability of pet_status
        pet_status = pet_data["pet_petstatus_id"] in (STATUS_AVAILABLE, STATUS_COMING_SOON)

        if pet_status:
            return True
        else:
            return False


    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)  # type: ignore

        client = PWAPI()
        pet = context["pet_data"]
        pet_id = pet["pet_id"]
        pet_loc_entity_id = pet["pet_loc_entity_id"]
        pet_price = pet["addon_pet_price"]
        is_pet_commerce_available = self.is_pet_commerce_available(pet)

        if not is_pet_commerce_available:
            context["is_pet_commerce_available"] = is_pet_commerce_available
            return context

        # Get addons and required addons
        resp = self.get_pet_addons(client, pet_id, pet_loc_entity_id)
        required_addon = self.get_required_addons(resp)

        deposit_amount = instance.glossary.get("deposit_amount", self.form.DEFAULT_DEPOSIT_AMOUNT)
        deposit_message = instance.glossary.get("deposit_message", self.form.DEFAULT_DEPOSIT_MESSAGE).replace("{deposit_amount}", "${:.2f}".format(deposit_amount))

        # Handle payment methods: deposit only, full payment only, both methods
        selected_payment_method = instance.glossary.get("payment_method", self.form.BOTH_METHODS)

        # Update context
        context.update({
            # General
            "pet_id": pet_id,
            "pet_loc_entity_id": pet_loc_entity_id,
            "pet_price": pet_price,
            "addons": resp,
            "required_addon": required_addon,
            "is_pet_commerce_available": is_pet_commerce_available,

            # Card Connect
            "cc_source": ''.join((self.frame_origin, self.get_frame_source(),)),
            "cc_origin": self.frame_origin,

            # Payment methods
            "deposit_amount": deposit_amount,
            "deposit_message": deposit_message,
            "only_deposit_payment": selected_payment_method == self.form.ONLY_DEPOSIT_PAYMENT,
            "only_full_payment": selected_payment_method == self.form.ONLY_FULL_PAYMENT,
            "both_payment_methods": selected_payment_method == self.form.BOTH_METHODS,

            # Other context
            "section_name": instance.glossary.get("section_name", self.form.DEFAULT_SECTION_NAME),
        })

        return context
