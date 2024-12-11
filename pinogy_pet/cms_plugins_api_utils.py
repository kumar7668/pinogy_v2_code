from typing import Dict, List, Set, Optional, Union
from django.core.cache import caches
from django.db.models.base import ModelBase
from django.db.models.query import QuerySet
# from . import pos_api, utils
from pos_api.pos_client import PWAPI
from bs4 import BeautifulSoup
from django.apps import apps
from typing import Dict, List, Set, Optional, Union
try:
    cache = caches['redis']
except:
    cache = caches['default']
    
# SETTINGS_FOR_PET_TYPE_CACHE_KEY = 'pinogy_available_pets:cms_plugins_api_utils:get_settings_for_pet_type:{pet_type_id}'
# SETTINGS_FOR_PET_TYPE_CACHE_TIMEOUT = 60 * 60


# def get_settings_for_pet_type(pet_type_id: int, client: pos_api.PWAPI) -> List[Dict]:
#     cache_key = SETTINGS_FOR_PET_TYPE_CACHE_KEY.format(pet_type_id=str(pet_type_id))
#     result = cache.get(cache_key)

#     if not result:
#         result = client.post_queries(**{
#             "quippet_name": 'read__tbl__pet_settings',
#             "quippet_params": {
#                 'qp_pstn_pet_type_id': pet_type_id,
#                 'qp_pstn_name': 'web.options.pettypes'
#             }
#         })['objects']
#         cache.set(cache_key, result, SETTINGS_FOR_PET_TYPE_CACHE_TIMEOUT)

#     return result


# PET_FILTERS_SORT_ORDER_CACHE_KEY = 'pinogy_available_pets:cms_plugins_api_utils:get_pet_filters_sort_order'
# PET_FILTERS_SORT_ORDER_CACHE_TIMEOUT = 60 * 60


# def get_pet_filters_sort_order(client: pos_api.PWAPI) -> List[Dict]:
#     result = cache.get(PET_FILTERS_SORT_ORDER_CACHE_KEY)
#     if result is None:
#         responce = client.post_queries(**dict(
#             quippet_name='read__qpt__list_pet_filters_ordered',
#             quippet_params=utils.get_base_quippet_params()
#         ))['objects']

#         result = []
#         filters_without_order = []
#         for item in responce:
#             if item['enabled']:
#                 if item['sort_order'] is None:
#                     filters_without_order.append({
#                         **item
#                     })
#                 else:
#                     result.append({
#                         **item
#                     })
#         if filters_without_order:
#             num = 0
#             filters_without_order = sorted(filters_without_order, key=lambda k: k['name'])
#             for item in filters_without_order:
#                 item['sort_order'] = len(result) + num
#                 result.append({
#                     **item
#                 })
#                 num += 1
#         cache.set(PET_FILTERS_SORT_ORDER_CACHE_KEY, result, PET_FILTERS_SORT_ORDER_CACHE_TIMEOUT)

#     return result


# PET_FILTERS_CUSTOM_FIELDS_CACHE_KEY = 'pinogy_available_pets:cms_plugins_api_utils:get_pet_filters_custom_fields'
# PET_FILTERS_CUSTOM_FIELDS_CACHE_TIMEOUT = 10 * 60


# def get_pet_filters_custom_fields(client: pos_api.PWAPI) -> List[Dict]:
#     result = cache.get(PET_FILTERS_CUSTOM_FIELDS_CACHE_KEY)

#     if result is None:
#         result = client.post_queries(**dict(
#             quippet_name='read__qpt__custom_fields',
#             quippet_params={
#                 'qp_cusfld_table_name': 'pets,pet_breeds,pet_litters,entity_pet_breeders',
#                 'columns': 'cusfld_table_name,cusfld_name,cusfld_type,cusfld_is_filter,cusfld_valid_data'
#             }
#         ))['objects']
#         cache.set(PET_FILTERS_CUSTOM_FIELDS_CACHE_KEY, result, PET_FILTERS_CUSTOM_FIELDS_CACHE_TIMEOUT)

#     return result


# PET_FILTERS_CACHE_KEY = 'pinogy_available_pets:cms_plugins_api_utils:get_pet_filters:{pet_type_name}&get_breeds:{breeds}&locations:{locations}'
# PET_FILTERS_CACHE_TIMEOUT = 10 * 60


# def get_pet_filters(
#         client: Optional[pos_api.PWAPI] = None,
#         pet_type_name: Optional[str] = None,
#         breeds_str: Optional[str] = None,
#         locations_str: Optional[str] = None
# ) -> Dict:
#     cache_key = PET_FILTERS_CACHE_KEY.format(
#         pet_type_name=pet_type_name.replace(' ', '_') if pet_type_name else '',
#         breeds=breeds_str.replace(' ', '_') if breeds_str else '',
#         locations=locations_str.replace(' ', '_') if locations_str else '',
#     )
#     result = cache.get(cache_key)

#     if result is None:
#         if client is None:
#             client = pos_api.PWAPI()

#         result = client.get_pet_filters(
#             ptype_name=pet_type_name,
#             pbrd_display_name=breeds_str,
#             pet_currently_at_entity_id=locations_str
#         )
#         cache.set(cache_key, result, PET_FILTERS_CACHE_TIMEOUT)

#     return result


# CREDOVA_INFO_CACHE_KEY = 'pinogy_available_pets:cms_plugins_api_utils:get_credova_info'
# CREDOVA_INFO_CACHE_TIMEOUT = 10 * 60


# def get_credova_info(client: Optional[pos_api.PWAPI] = None) -> Dict:
#     result = cache.get(CREDOVA_INFO_CACHE_KEY)

#     if result is None:
#         if not client:
#             client = pos_api.PWAPI()

#         result = client.get_store_codes()
#         cache.set(CREDOVA_INFO_CACHE_KEY, result, CREDOVA_INFO_CACHE_TIMEOUT)

#     return result


# AVAILABLE_PETS_CACHE_KEY = 'pinogy_available_pets:cms_plugins_api_utils:get_available_pets:{pet_type_names}:locations:{locations}:pet_status_id:{pet_status_id}'
# AVAILABLE_PETS_CACHE_TIMEOUT = 5 * 60


# def get_available_pets(
#     pet_type_names: Optional[Union[List[str], str]] = None,
#     client: Optional[pos_api.PWAPI] = None,
#     location_ids: Optional[List[int]] = None,
#     pet_status_id: Optional[str] = None,
#     order_by: Optional[str] = None,
#     offset: Optional[int] = None,
#     limit: Optional[int] = None,
# ) -> Dict:
#     if pet_type_names is not None:
#         if not isinstance(pet_type_names, list):
#             pet_type_names = [pet_type_names]
#     pet_type_names_joined = ','.join(pet_type_names) if pet_type_names else None
#     location_joined = ','.join(str(loc) for loc in location_ids) if location_ids else None
#     cache_key = AVAILABLE_PETS_CACHE_KEY.format(pet_type_names=pet_type_names_joined, locations=location_joined, pet_status_id=pet_status_id)
#     result = cache.get(cache_key)

#     if result is None:
#         if not client:
#             client = pos_api.PWAPI()

#         quippet_params = utils.get_base_quippet_params()
#         quippet_params["qp_pet_has_image"] = True

#         if pet_type_names_joined:
#             quippet_params["qp_ptype_name"] = pet_type_names_joined
#         if location_joined:
#             quippet_params['qp_pet_currently_at_entity_id'] = location_joined
#         if pet_status_id:
#             quippet_params['qp_pet_sub_status_id'] = pet_status_id
#         if order_by:
#             quippet_params['order_by'] = order_by
#         if offset:
#             quippet_params['offset'] = offset
#         if limit:
#             quippet_params['limit'] = limit


#         result = client.get_pets(**dict(
#             quippet_params=quippet_params
#         )).get('pets', [])
#         cache.set(cache_key, result, AVAILABLE_PETS_CACHE_TIMEOUT)

#     return result


# BREED_AVAILABLE_PETS_CACHE_KEY = 'pinogy_available_pets:cms_plugins_api_utils:get_breed_available_pets:{breed_slug}_{location_ids}'
# BREED_AVAILABLE_PETS_CACHE_TIMEOUT = 5 * 60


# def get_breed_available_pets(breed_slug: str, client: Optional[pos_api.PWAPI] = None, locations: Optional[List[str]] = None) -> Dict:
#     cache_key = BREED_AVAILABLE_PETS_CACHE_KEY.format(breed_slug=breed_slug, location_ids=locations)
#     result = cache.get(cache_key)

#     if result is None:
#         if not client:
#             client = pos_api.PWAPI()
            
#         kwargs = {
#             "breed_slug": breed_slug,
#             "show_other_if_missing": True,
#             "location_ids": locations or [],
#             "force_json": True
#         }

#         result = client.get_available_pets(
#             **kwargs
#         )['objects']
#         cache.set(cache_key, result, BREED_AVAILABLE_PETS_CACHE_TIMEOUT)

#     return result

# SIMILAR_PETS_CACHE_KEY = 'pinogy_available_pets:cms_plugins_api_utils:get_similar_pets:{breed_slug}_{location_ids}'
# SIMILAR_PETS_CACHE_TIMEOUT = 5 * 60


# def get_similar_pets(breed_slug: str, client: Optional[pos_api.PWAPI] = None, locations: Optional[List[str]] = None) -> List[Dict]:
#     cache_key = SIMILAR_PETS_CACHE_KEY.format(breed_slug=breed_slug, location_ids=locations)
#     result = cache.get(cache_key)

#     if result is None:
#         if not client:
#             client = pos_api.PWAPI()
            
#         kwargs = {
#             "breed_slug": breed_slug,
#             "location_ids": locations or [],
#             "force_json": True
#         }

#         result = client.get_similar_pets(**kwargs)['objects']
#         cache.set(cache_key, result, SIMILAR_PETS_CACHE_TIMEOUT)

#     return result


# BREEDS_LIST_CACHE_KEY = 'pinogy_available_pets:cms_plugins_api_utils:get_breeds_list:{pet_type_slug}:available:{flag}:loc:{location}:ptype:{ptype}:search_val:{search_val}'
# BREEDS_LIST_CACHE_TIMEOUT = 60 * 60


# def get_breeds_list(
#     pet_type_slug: Optional = None,
#     client: Optional[pos_api.PWAPI] = None,
#     available_only: bool = False,
#     pet_location_id: Optional[List[int]] = None,
#     pet_type_id: Optional[List[int]] = None,
#     search_val= None
# ) -> Dict:
#     cache_key = BREEDS_LIST_CACHE_KEY.format(
#         pet_type_slug=pet_type_slug if pet_type_slug else '',
#         flag=available_only,
#         location=str(pet_location_id) if pet_location_id else '',
#         ptype=str(pet_type_id) if pet_type_id else '',
#         search_val=str(search_val) if search_val else ''
#     )
    
#     result = cache.get(cache_key)
#     if result is None:
#         if not client:
#             client = pos_api.PWAPI()

#         kwargs = {'to_be_displayed': True}

#         if pet_location_id:
#             kwargs['to_be_displayed'] = {"location_ids": pet_location_id}

#         for key, value in (
#             ('pet_type_slug', pet_type_slug),
#             # ('pet_location_id', pet_location_id),
#             ('pet_type_id', pet_type_id),
#         ):
#             if value:
#                 kwargs[key] = value

#         if available_only:
#             kwargs['pet_status_id'] = -1
        
#         if search_val:
#             kwargs['display_name_like'] = search_val

#         result = client.get_breeds(**kwargs)['objects']
#         cache.set(cache_key, result, BREEDS_LIST_CACHE_TIMEOUT)

#     return result


# BREED_CACHE_KEY = 'pinogy_available_pets:context_utils:fill_breed:{breed_slug}'
# BREED_CACHE_TIMEOUT = 60 * 60


# def get_breed(breed_slug: str, client: Optional[pos_api.PWAPI] = None) -> Dict:
#     cache_key = BREED_CACHE_KEY.format(breed_slug=breed_slug)
#     breed = cache.get(cache_key)

#     if not breed:
#         if client is None:
#             client = pos_api.PWAPI()
#         breed = client.get_breed(slug=breed_slug)
#         cache.set(cache_key, breed, BREED_CACHE_TIMEOUT)

#     return breed


# LOCATIONS_CACHE_KEY = 'pinogy_available_pets:cms_plugins_api_utils:get_locations'
# LOCATIONS_CACHE_TIMEOUT = 10 * 60


# def get_locations(client: Optional[pos_api.PWAPI] = None) -> Dict:
#     result = cache.get(LOCATIONS_CACHE_KEY)

#     if result is None:
#         if not client:
#             client = pos_api.PWAPI()

#         result = client.get_locations()
#         cache.set(LOCATIONS_CACHE_KEY, result, LOCATIONS_CACHE_TIMEOUT)

#     return result


# STORES_CACHE_KEY = 'pinogy_available_pets:cms_plugins_api_utils:get_stores'
# STORES_CACHE_TIMEOUT = 10 * 60


# def get_stores(client: Optional[pos_api.PWAPI] = None) -> List[Dict]:
#     result = cache.get(STORES_CACHE_KEY)

 #     if result is None:
#         if not client:
#             client = pos_api.PWAPI()

#         # result = client.get_stores()['objects']
#         result = client.get_website_data(fields_include=['locations'])['locations']
#         cache.set(STORES_CACHE_KEY, result, STORES_CACHE_TIMEOUT)

#     return result


# STORE_DETAIL_CACHE_KEY = 'pinogy_available_pets:cms_plugins_api_utils:get_store_detail:{store_slug}'
# STORE_DETAIL_TIMEOUT = 10 * 60


# def get_store_detail(
#     store_slug: str,
#     client: Optional[pos_api.PWAPI] = None
# ) -> Dict:
#     cache_key = STORE_DETAIL_CACHE_KEY.format(store_slug=store_slug)

#     result = cache.get(cache_key)

#     if result is None:
#         if not client:
#             client = pos_api.PWAPI()

#         result = {}
#         quippet_params = utils.get_base_quippet_params()
#         quippet_params.update({'qp_loc_is_enabled': True, 'qp_loc_available_publicly': True})

#         quippet_params['qp_loc_slug'] = store_slug

#         api_result = client.post_queries(**dict(
#             quippet_name='read__qpt__loc_doc',
#             quippet_params=quippet_params
#         ))

#         store_list = api_result.get('objects', [])
#         if len(store_list) > 0:
#             result = store_list[0].get('loc_doc')

#         cache.set(cache_key, result, STORE_DETAIL_TIMEOUT)

#     return result


# PET_TYPE_LIST_CACHE_KEY = 'pinogy_available_pets:cms_plugins_api_utils:get_pet_type_list'
# PET_TYPE_LIST_CACHE_TIMEOUT = 10 * 60


# def get_pet_type_list(client: Optional[pos_api.PWAPI] = None) -> List[Dict]:
#     result = cache.get(PET_TYPE_LIST_CACHE_KEY)

#     if not result:
#         if client is None:
#             client = pos_api.PWAPI()
#         result = []
#         for item in client.get_pet_types()['objects']:
#             if item['is_enabled'] and not item['deleted']:
#                 result.append(item)
#         cache.set(PET_TYPE_LIST_CACHE_KEY, result, PET_TYPE_LIST_CACHE_TIMEOUT)

#     return result


# def get_pet_type_by_slug(pet_type_slug: str, client: Optional[pos_api.PWAPI] = None) -> Optional[Dict]:
#     pet_type_list = get_pet_type_list(client)
#     for item in pet_type_list:
#         if item['slug'] == pet_type_slug:
#             return item


# INTEGRATION_SETTINGS_CACHE_KEY = 'pinogy_available_pets:cms_plugins_api_utils:get_integration_settings'
# INTEGRATION_SETTINGS_CACHE_TIMEOUT = 24 * 60


# def get_integration_settings() -> Dict:
#     result = cache.get(INTEGRATION_SETTINGS_CACHE_KEY)

#     if not result:
#         client = pos_api.PWAPI()
#         result = client.get_integration_settings()['objects']
#         cache.set(INTEGRATION_SETTINGS_CACHE_KEY, result, INTEGRATION_SETTINGS_CACHE_TIMEOUT)

#     return result


# def get_shopwindow_integration_settings() -> Optional[Dict]:
#     integrations = get_integration_settings()

#     for item in integrations:
#         # 18 is value for shopwindow integration in POS
#         if item['intstn_integration_id'] == 18:
#             return item['intstn_attrs']

#     return None


def get_list_of_ad_cards(pet_type_id):
    # Function return list of info about ad cards, not the ad cards themselves
    result = []
    client = PWAPI()
    data = client.get_pet_types_adcard(pet_type_id=pet_type_id)
    if "objects"in data and data['objects']:
        for ad_card in data['objects']:
            if ad_card['type'] == 'image':
                result.append({
                    'id': ad_card['image']['id'],
                    'sort_order': ad_card['sort_order'],
                    'deleted': ad_card['deleted'],
                    'file_type': 0,
                    "ad_card_link": ad_card['url'],
                })
            elif ad_card['type'] == 'video':
                url_html = ad_card['video']['embed_html']
                if url_html:
                    soup = BeautifulSoup(url_html, 'html.parser')
                    result.append({
                        'id': ad_card['video']['file']['id'],
                        'sort_order': ad_card['sort_order'],
                        'deleted': ad_card['deleted'],
                        'file_type': 1,
                        'url': soup.iframe['src'],
                        "ad_card_link": ad_card['url'],
                    })
    return result


def get_ad_card(file_id):
    client = PWAPI()

    result = client.get_file([file_id])
    return result


# PET_API_VIDEO_CACHE_KEY = 'pinogy_available_pets:cms_plugins_api_utils:get_videos_media:{pet_id}'
# PET_API_VIDEO_CACHE_TIMEOUT = 60 * 60


# def get_videos_media(pet_id):
#     cache_key = PET_API_VIDEO_CACHE_KEY.format(pet_id=pet_id)
#     result = cache.get(cache_key)
#     if not result:
#         result = []
#         client = pos_api.PWAPI()
#         # Call API for get Vimeo`s META
#         data = client.get_videos_meta(pet_id=pet_id)
#         if data['objects']:
#             for video in data['objects']:
#                 # Get iframe from Vimeo`s META
#                 url_html = video['video']['embed_html']
#                 if url_html:
#                     # Parse iframe by BeautifulSoup, for get vimeo src
#                     soup = BeautifulSoup(url_html, 'html.parser')
#                     item = {
#                         'video_url': soup.iframe['src'],
#                         'video_id': video['video']['id'],
#                         'sort_order': video['sort_order'],
#                         'alt': video['description']
#                     }
#                     result.append(item)
#         cache.set(cache_key, result, PET_API_VIDEO_CACHE_TIMEOUT)
#     return result


# PET_API_PHOTO_CACHE_KEY = 'pinogy_available_pets:cms_plugins_api_utils:get_photos_media:{pet_id}'
# PET_API_PHOTO_CACHE_TIMEOUT = 60 * 60


# def get_photos_media(pet_id):
#     cache_key = PET_API_PHOTO_CACHE_KEY.format(pet_id=pet_id)
#     result = cache.get(cache_key)

#     if result:
#         return False, result
#     else:
#         result = []
#         client = pos_api.PWAPI()
#         # Call API for get photos META
#         data = client.get_photos_meta(pet_id=pet_id)
#         if data['objects']:
#             for item in data['objects']:
#                 item = {
#                     'photo_id': int(item['image']['id']),
#                     'sort_order': int(item['sort_order'])
#                 }
#                 result.append(item)
#         cache.set(cache_key, result, PET_API_PHOTO_CACHE_TIMEOUT)
#         return True, result


# def get_pet_photos(
#     photo_id_list: Set[Optional[int]], image_model: ModelBase, client: Optional[pos_api.PWAPI] = None
# ) -> Dict:

#     def get_non_existed_id_list(queryset: QuerySet) -> Set[int]:
#         db_id_list = queryset.values_list('file_id', flat=True)
#         return {id for id in photo_id_list if id not in db_id_list}

#     def handle_fetched_photo(api_obj: Dict) -> None:
#         image_model.objects.create(
#             order=0,
#             file_name='{}.{}'.format(
#                 api_obj['file_orig_basename'].replace(' ', '-'),
#                 api_obj['file_orig_extension']
#             ),
#             file_extension=api_obj['file_orig_extension'],
#             file_id=int(api_obj['file_id']),
#         ).save_file(
#             photo=api_obj['flin_contents'].encode('utf-8')
#         )

#     def fetch_api_photos(
#         id_set: Set[int], pos: Optional[pos_api.PWAPI] = None
#     ) -> None:
#         if not pos:
#             pos = pos_api.PWAPI()
#         response = pos.get_file(pet_type_id=list(id_set))
#         for obj in response.get('objects', []):
#             handle_fetched_photo(api_obj=obj)

#     def get_result(queryset: QuerySet) -> Dict:
#         result_dict = {}
#         for db_data in queryset.all():
#             result_dict[str(db_data.file_id)] = dict(
#                 file_id=db_data.file_id,
#                 alt=db_data.alt if db_data.alt else '',
#                 file_image=db_data.url()
#             )
#         return result_dict

#     q_set = image_model.objects.filter(file_id__in=photo_id_list)
#     non_existed_set = get_non_existed_id_list(queryset=q_set)
#     if non_existed_set:
#         fetch_api_photos(id_set=non_existed_set, pos=client)
#     return get_result(queryset=q_set)

# def get_pet_images(file_ids, pet_id, is_badges=False):
#     ApiPetPhoto = apps.get_model('pinogy_available_pets', 'ApiPetPhoto')
    
#     client = pos_api.PWAPI()
#     items = client.post_queries_without_cache(**{
#             "quippet_name": 'read__tbl__vw_files_with_in_band_contents',
#             "quippet_params": {
#                 'qp_file_id': ','.join(str(item) for item in file_ids)
#             }
#         })['objects']

#     result = []
#     for item in items:
#         # to avoid duplicate image start
#         if is_badges:
#             pet_id=0
#         # end
#         # item_obj, created = ApiPetPhoto.objects.get_or_create(file_id=item['file_id'], pet_id=pet_id, is_badges=is_badges)
#         # if created:
#         #     file_data = item['flin_contents'].encode('utf-8')
#         #     item_obj.file_extension = item['file_orig_extension']
#         #     item_obj.alt = item['file_description']
#         #     item_obj.save()
#         #     item_obj.save_file(file_data)
#         #     result.append(item_obj)

#         item_obj = ApiPetPhoto.objects.filter(file_id=item['file_id']).first()
#         if not item_obj:
#             item_obj = ApiPetPhoto.objects.create(file_id=item['file_id'],pet_id=pet_id,is_badges=is_badges)
#         if item_obj:
#             file_data = item['flin_contents'].encode('utf-8')
#             item_obj.file_extension = item['file_orig_extension']
#             item_obj.alt = item['file_description']
#             item_obj.save()
#             item_obj.save_file(file_data)
#             result.append(item_obj)

#     return result

# def add_pet_image(file_ids, pet_id):
#     # TODO: Handle if there is no image
#     if file_ids:
#         ApiPetPhoto = apps.get_model('pinogy_available_pets', 'ApiPetPhoto')
#         try:
#             img = ApiPetPhoto.objects.filter(file_id = file_ids[0], pet_id=pet_id)
#             if img:
#                 img = img.first()
#                 return img.url(), img.alt
#             else:
#                 pet_imgs = get_pet_images(file_ids, pet_id)
#                 return pet_imgs[0].url(), pet_imgs[0].alt if pet_imgs else ''
#         except ApiPetPhoto.DoesNotExist:
#             return '', ''

#     return None, ''

# def add_pet_images(file_ids, pet_id):
#     if file_ids:
#         ApiPetPhoto = apps.get_model('pinogy_available_pets', 'ApiPetPhoto')
#         try:
#             img = ApiPetPhoto.objects.filter(file_id__in= file_ids, pet_id=pet_id)
#             if img:
#                 return img
#             else:
#                 pet_imgs = get_pet_images(file_ids, pet_id)
#                 return  pet_imgs
#         except ApiPetPhoto.DoesNotExist:
#             return ''

#     return None 


# def add_pet_badges(file_ids, pet_id):
#     if file_ids:
#         ApiPetPhoto = apps.get_model('pinogy_available_pets', 'ApiPetPhoto')
#         try:
#             img = ApiPetPhoto.objects.filter(file_id__in = file_ids, is_badges=True)
#             if img and len(img)==len(file_ids):
#                 return [pet.url() for pet in img]
#             else:
#                 pet_imgs = get_pet_images(file_ids, pet_id, is_badges=True)
#                 return [pet.url() for pet in pet_imgs]
#         except ApiPetPhoto.DoesNotExist:
#             return ''

#     return None 