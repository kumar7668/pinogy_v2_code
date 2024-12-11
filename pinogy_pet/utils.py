import datetime
import pytz

from typing import Optional, Dict, Any, Union, List
from django.templatetags.static import static
from django.core.cache import cache
from django.utils.dateparse import parse_datetime
from collections import defaultdict

from pinogy_shop.models import images
from pos_api.pos_client import PWAPI
from pos_api.cached_response import get_locations_timezone

STATUS_AVAILABLE = -1
STATUS_ON_HOLD = -2
STATUS_ISOLATION = -3
STATUS_EXCEPTION = -4
STATUS_SOLD = -5
STATUS_ON_LAYAWAY = -6
STATUS_COMING_SOON = -7

def get_pet_data(client, pet_id):
    CACHE_KEY = f"addon_pet_data_{pet_id}"
    pet_data = cache.get(CACHE_KEY)

    if not pet_data:
        pet_data = client.get_pet_data(pet_id=pet_id)
        cache.set(CACHE_KEY, pet_data, 60)

    return pet_data

def get_pet_price(client: PWAPI, pet_id : int) -> str:
    pet_data = get_pet_data(client, pet_id=pet_id)
    pet_price = pet_data['sale_price']
    if pet_price in ['0.00', '0'] or not pet_price:
        pet_price = pet_data['price']
    
    return pet_price

def get_addon_image_url(product_id : Optional[int] = None, image_id : Optional[int] = None) -> Union[Dict, images.ProductImage]:
    """
    return image url from productimage table if available
    else return static image url 
    """
    addon_image : Optional[Union[Dict, images.ProductImage]] = None 
    if product_id and image_id:
        addon_image = images.ProductImage.objects.get_first_image_from_db(
                    product_id, image_id)
    
    if not addon_image:
        addon_image = {
            'placeholder': True,
            'url': static('pinogy_shop/img/default-product.png')
        }

    return addon_image


PET_API_PHOTO_CACHE_KEY = 'pinogy_pets:utils:get_photos_meta:{pet_id}'
PET_API_PHOTO_CACHE_TIMEOUT = 60 * 60

def get_photos_meta(client, pet_id):
    
    cache_key = PET_API_PHOTO_CACHE_KEY.format(pet_id=pet_id)
    result = cache.get(cache_key)

    if result:
        return result
    else:
        data = client.get_photos_meta(pet_id=pet_id)
        result = data['objects']
        cache.set(cache_key, result, PET_API_PHOTO_CACHE_TIMEOUT)
        return result
    
PET_API_VIDEO_CACHE_KEY = 'pinogy_pets:utils:get_videos_meta:{pet_id}'
PET_API_VIDEO_CACHE_TIMEOUT = 60 * 60

def get_videos_meta(client, pet_id):
    
    cache_key = PET_API_VIDEO_CACHE_KEY.format(pet_id=pet_id)
    result = cache.get(cache_key)

    if result:
        return result
    else:
        data = client.get_videos_meta(pet_id=pet_id)
        result = data['objects']
        cache.set(cache_key, result, PET_API_VIDEO_CACHE_TIMEOUT)
        return result

PET_FILTERS_CACHE_KEY = 'pinogy_pet:utils:get_pet_filters:{pet_type_name}&get_breeds:{breeds}&locations:{locations}&pet_loc_entity_id:{pet_loc_entity_id}'
PET_FILTERS_CACHE_TIMEOUT = 10 * 60

def get_pet_filters(
        client: Optional[PWAPI] = None,
        pet_type_name: Optional[str] = None,
        breeds_str: Optional[str] = None,
        locations_str: Optional[str] = None,
        pet_loc_entity_id: Optional[List[str]] = None
) -> Dict:
    cache_key = PET_FILTERS_CACHE_KEY.format(
        pet_type_name=pet_type_name.replace(' ', '_') if pet_type_name else '',
        breeds=breeds_str.replace(' ', '_') if breeds_str else '',
        locations=locations_str.replace(' ', '_') if locations_str else '',
        pet_loc_entity_id=pet_loc_entity_id if pet_loc_entity_id else '',
    )
    result = cache.get(cache_key)

    if result is None:
        if client is None:
            client = PWAPI()

        result = client.get_pet_filters(
            ptype_name=pet_type_name,
            pbrd_display_name=breeds_str,
            pet_currently_at_entity_id=locations_str,
            pet_loc_entity_id=pet_loc_entity_id
        )
        cache.set(cache_key, result, PET_FILTERS_CACHE_TIMEOUT)

    return result

def get_play_date_schedule(client, pet):

    # if pet status is in STATUS_AVAILABLE = -1, STATUS_ON_HOLD = -2, STATUS_ISOLATION = -3, STATUS_EXCEPTION = -4
    # then only we shows schedule a play date
    if pet['pet_petstatus_id'] not in [STATUS_AVAILABLE, STATUS_ON_HOLD, STATUS_ISOLATION, STATUS_EXCEPTION]:
        return {}

    start_at = datetime.date.today()
    finish_at = start_at + datetime.timedelta(days=3)
    location_id = pet['pet_loc_entity_id']

    r = client.get_pet_box_visits_schedule(start_at=start_at, finish_at=finish_at, location_id=location_id)
    result = r.get('objects', [])
    if result:
        # get the location timezone
        location_timezone = get_locations_timezone(client).get(location_id)

        data_filtered = []
        now = datetime.datetime.now(pytz.utc)
        for item in result:
            start_at = parse_datetime(item['start_at'])
            if start_at < now:
                continue

            # Convert timezone if available
            if location_timezone:
                item['start_at'] = datetime.datetime.fromisoformat(item['start_at']).astimezone(pytz.timezone(location_timezone)).isoformat()
                item['finish_at'] = datetime.datetime.fromisoformat(item['finish_at']).astimezone(pytz.timezone(location_timezone)).isoformat()

            data_filtered.append(item)
        result = data_filtered

    data = result

    # Dictionary to store events categorized by start date
    categorized_data = defaultdict(list)

    for event in data:
        start_time = datetime.datetime.fromisoformat(event["start_at"]).time()
        end_time = datetime.datetime.fromisoformat(event["finish_at"]).time()
        s_time = datetime.datetime.fromisoformat(event["start_at"])
        e_time = datetime.datetime.fromisoformat(event["finish_at"])
        start_date = datetime.datetime.fromisoformat(event["start_at"]).date().strftime("%a %b %d %Y").upper()
        categorized_data[start_date].append({"start_time": start_time.strftime("%I:%M %p"), 
                                             "end_time": end_time.strftime("%I:%M %p"),
                                             "s_time": s_time.strftime('%Y-%m-%dT%H:%M:%S%z'),
                                             "e_time": e_time.strftime('%Y-%m-%dT%H:%M:%S%z')})

    # Convert to dictionary for JSON serialization
    categorized_dict = {date: times for date, times in categorized_data.items()}   

    return categorized_dict