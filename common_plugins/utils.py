from typing import Dict, List, Optional
from django.core.cache import cache
from datetime import datetime

from pos_api.pos_client import PWAPI
from django.utils import timezone
from .models import InstagramData, InstagramFeedPluginModel
import requests

MINIMUM_DAYS_TO_FETCH_FEEDS = 1
def get_stores_data(client: PWAPI) -> List[Dict[str, str]]:
    result = cache.get('STORE_DATA_CACHE_KEY')

    if result is None:
        store_data = client.get_website_data()
        store_location = store_data['locations']

        result = []

        for store in store_location:
            if store.get('is_enabled') and store.get('is_public'):
                # We are getting different keys like Office, Work, Mobile in contact_numbers from POS
                # So, we adding first contact number from `contact_numbers` in store data, we can simply use it without checking it every place
                if store['entity'].get('contact_numbers', {}):
                    store['store_contact'] = next((value for value in store['entity']['contact_numbers'].values() if value), None)
                else:
                    store['store_contact'] = None
                result.append(store)
        
        cache.set('STORE_DATA_CACHE_KEY', result, 60 * 60)

    return result

def get_primary_store_data(client: PWAPI) -> Dict[str, str]:
    """
    return primary location if available
    else returns blank dict is location is not enabled in POS
    """
    result = cache.get('PRIMARY_STORE_DATA_CACHE_KEY')

    if result is None:
        stores_data = get_stores_data(client=client) 

        primary_store = [store for store in stores_data if store.get("is_primary_store") ]
        if primary_store:
            result = primary_store[0]
        elif stores_data:
            result = stores_data[0]
        else: 
            result = {}

        cache.set('PRIMARY_STORE_DATA_CACHE_KEY', result, 60 * 60)

    return result

def get_selected_store(client: PWAPI, store_id : Optional[int] = None) -> Dict[str, str]:
    """
    set store based on store_id if available
    else set primary store as selected store
    else set first store from data if above both not available

    returns blank dict is location is not enabled in POS
    """
    CACHE_KEY = f'SELECTED_STORE_DATA_CACHE_KEY_{store_id}'
    store = cache.get(CACHE_KEY)

    if store is None:
        stores_data = get_stores_data(client=client)

        if store_id:
            store = [ store for store in stores_data if store.get("id") == int(store_id) ]
        
        if not store: 
            store = [ store for store in stores_data if store.get("is_primary_store") ]
        
        if store:
            store = store[0]
        elif stores_data:
            store = stores_data[0]
        else:
            store = {}

        cache.set(CACHE_KEY, store, 60 * 60)

    return store

def convert_to_12hr_format(times):
    """
        take the working hours and return it in 12hr format
        times should be ["13:00:00", "20:00:00"] or ["9:00 AM", "8:00 PM"]
    """
    # Check if the input is a list
    if not isinstance(times, list):
        return times
    
    converted_times = []

    for time_str in times:
        if 'AM' not in time_str and not 'PM' in time_str:
            try:
                time_obj = datetime.strptime(time_str, '%H:%M:%S')
                converted_time_str = time_obj.strftime('%I:%M %p')
            except Exception as e:
                converted_time_str = time_str          
            converted_times.append(converted_time_str)
        else:
            converted_times.append(time_str)

    return converted_times

def convert_to_24hr_format(times):
    """
    Take the working hours and return them in 24hr format.
    Times should be ["13:00:00", "8:00 PM"] or ["1:00 PM", "8:00 PM"].
    """
    # Check if the input is a list
    if not isinstance(times, list):
        return times
    converted_times = []
    for time_str in times:
        if 'AM' in time_str or 'PM' in time_str:
            try:
                time_obj = datetime.strptime(time_str, '%I:%M %p')
                converted_time_str = time_obj.strftime('%H:%M:%S')
            except Exception as e:
                converted_time_str = time_str
            converted_times.append(converted_time_str)
        else:
            converted_times.append(time_str)
    return converted_times

def is_shopwindow_enable(store_id):
    client = PWAPI()  
    # Retrieve website data, including shop window location IDs
    website_data = client.get_website_data(fields_include=['shopwindow_location_ids'])
    shop_window_ids = website_data.get('shopwindow_location_ids', [])
    return store_id in shop_window_ids

def get_shopwindow_location_ids():
    client = PWAPI()
    # Retrieve website data, including shop window location IDs
    website_data = client.get_website_data(fields_include=['shopwindow_location_ids'])
    shop_window_location_ids = website_data.get('shopwindow_location_ids', [])
    return shop_window_location_ids


def instagram_data(access_token, plugin_id):
    """
    Fetches Instagram data for a given access token and plugin ID.
    
    Args:
    access_token (str): Instagram access token.
    plugin_id (int): ID of the Instagram feed plugin.
    
    Returns:
    list: List of InstagramData objects.
    """
    try:
        cache_key = f"common_plugins:instagram_data:{plugin_id}:{access_token}"
        if result := cache.get(cache_key):
            return result
        
        plugin = InstagramFeedPluginModel.objects.get(cmsplugin_ptr_id=plugin_id)
        
        # Check if it's necessary to fetch new feeds or use existing ones
        if not check_latest_insta_feeds(plugin):
            posts = InstagramData.objects.filter(plugin=plugin)
        else:
            posts = get_latest_insta_feeds(plugin, access_token)

        # Cache the fetched data for 24 hours
        cache.set(cache_key, posts, 60 * 60 * 24)
        return posts
    except Exception as e:
        print("An error has occurred:",e)
        return []

def check_latest_insta_feeds(plugin) -> bool:
    """
    Checks if it's necessary to fetch new Instagram feeds.
    
    Args:
    plugin (InstagramFeedPluginModel): Instagram feed plugin object.
    
    Returns:
    bool: True if new feeds need to be fetched, False otherwise.
    """
    last_feed = InstagramData.objects.filter(plugin=plugin).last()
    if last_feed:
        days_difference = (timezone.now().date() - last_feed.created_at).days
        if days_difference < MINIMUM_DAYS_TO_FETCH_FEEDS:
            return False
        
    return True

def get_latest_insta_feeds(plugin, access_token) -> list:
    """
    Fetches the latest Instagram feeds for a given plugin.
    
    Args:
    plugin (InstagramFeedPluginModel): Instagram feed plugin object.
    access_token (str): Instagram access token.
    
    Returns:
    list: List of dictionaries representing Instagram posts.
    """
    try:
        all_posts = []
        base_url = "https://graph.instagram.com/me/media"
        params = {
            "fields": "id,permalink,media_url,caption",
            "access_token": access_token
        }
        while True:
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                posts = data.get("data", [])
                all_posts.extend(posts)
                if 'paging' in data and 'next' in data['paging']:
                    next_url = data['paging']['next']
                    base_url = next_url
                else:
                    break
            else:
                print(f"Error: {response.status_code}")
                break

        # Get all existing post_ids for the specified plugin
        existing_post_ids = set(InstagramData.objects.filter(plugin=plugin).values_list('post_id', flat=True))

        # Create new rows for the new data
        for post in all_posts:
            if post['id'] not in existing_post_ids:
                InstagramData.objects.create(
                    plugin=plugin,
                    post_id=post['id'],
                    permalink=post['permalink'],
                    media_url=post['media_url'],
                    caption=post.get('caption', ''),
                )

        return InstagramData.objects.filter(plugin=plugin)
    except Exception as e:
        print("An error has occurred:",e)
        return []

def int_to_base36(num):
    if num < 0:
        raise ValueError("Positive integers only")

    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base36 = ""

    while num:
        num, i = divmod(num, 36)
        base36 = digits[i] + base36

    return base36 or digits[0]

def base36_to_int(base36):
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base36 = base36.upper().strip()  # Ensure input is in uppercase and stripped of whitespace
    num = 0

    for char in base36:
        num = num * 36 + digits.index(char)

    return num
