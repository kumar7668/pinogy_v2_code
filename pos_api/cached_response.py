from typing import Optional
from django.core.cache import cache

from pos_api.pos_client import PWAPI

def get_pos_integration_data(client: Optional[PWAPI] = None):

    cache_key = "web_integration_data:cached_response:get_pos_integration_data"

    if result := cache.get(cache_key):
        return result

    if not client:
        client = PWAPI()
    
    pos_integration_data = client.get_website_data()

    # set default values
    pos_integration_data["out_of_stock_message"] = ( pos_integration_data.get("out_of_stock_message") or "This item is currently out of stock." )
    pos_integration_data["special_order_message"] = ( pos_integration_data.get("special_order_message") or "Special Order Item. Available in 3-7 days." )

    cache.set(cache_key, pos_integration_data, 60 * 60 * 24 * 7) # caching for one week

    return pos_integration_data

def get_locations_timezone(client: Optional[PWAPI] = None):
    cache_key = f'get_locations_timezone:timezone_data'

    # Try to get the data from the cache
    timezone_data = cache.get(cache_key)
    if timezone_data is not None:
        return timezone_data
    
    if client is None:
        client = PWAPI()
    
    # If not in cache, fetch the data
    timezone_data = {
        location['id']: location['timezone']
        for location in client.get_website_data().get('locations', [])
        if 'id' in location and 'timezone' in location
    }

    # Cache the data for month
    cache.set(cache_key, timezone_data, timeout=60 * 60 * 24 * 30) 

    return timezone_data