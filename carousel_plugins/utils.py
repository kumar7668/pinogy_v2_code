from typing import Any, Dict, List, Optional, Union

from django.core.cache import cache

from pos_api import utils
from pos_api.pos_client import PWAPI
from . import models


def get_pet_type_list(client):
    pet_type_uniqe_list = cache.get("pet_type_uniqe_list")
    if not pet_type_uniqe_list:
        pet_type_uniqe_list = client.get_pet_types()["objects"]
        cache.set("pet_type_uniqe_list", pet_type_uniqe_list, 60 * 60)

    return pet_type_uniqe_list


def get_pet_status_list(client):
    pet_status_list = cache.get("pet_status_list")
    if not pet_status_list:
        pet_status_list = client.get_pets_status_list()["objects"]
        cache.set("pet_status_list", pet_status_list, 60 * 60)

    return pet_status_list


def get_locations_list(client):
    locations_list = cache.get("locations_list")
    if not locations_list:
        locations_list = client.get_locations()["objects"]
        cache.set("locations_list", locations_list, 60 * 60)

    return locations_list

def get_brands_data(client):
    result = cache.get('PRODUCTS_BRANDS_CACHE_KEY')
    if result is None:
        result = client.get_brands_details()["objects"]        
        cache.set('PRODUCTS_BRANDS_CACHE_KEY', result, 60 * 60 * 24 * 7)
    return result

def get_brand_image_from_db(client, brand_id, brand_image_id=None):
    if brand_image_id:
        img_obj = models.BrandImage.objects.filter(brand_id=brand_id, brand_image_id=brand_image_id).first()
        if img_obj:
            image = img_obj
        else:
            result = client.get_brand_image(brand_id, brand_image_id)
            if result:
                new_img_obj = models.BrandImage.objects.create(brand_id=brand_id, brand_image_id=brand_image_id, file_extension=result['file']['extension'])
                new_img_obj.save_file(result['filedata'].encode('utf-8'))
                new_img_obj.save()
                image = new_img_obj
    else:
        image = { "url" : "/static/images/default-placeholder-image.webp" }
    return image


def get_promotions_data(client):
    result =cache.get('PRODUCTS_PROMOTIONS_CACHE_KEY')
    if result is None:
        result = client.get_promotions_list()["objects"]        
        cache.set('PRODUCTS_PROMOTIONS_CACHE_KEY', result, 60 * 60)
    return result

def get_promotions_data_carousel(client,kind:None):
    result =cache.get('PRODUCTS_PROMOTIONS_CACHE_KEY')
    if True:
        result = client.get_promotions_list(kind)["objects"]        
        cache.set('PRODUCTS_PROMOTIONS_CACHE_KEY', result, 60 * 60)
    return result

def get_promotion_image_from_db(client, promotion_id, promotion_image_id=None):
    if promotion_image_id:
        img_obj = models.PromotionImage.objects.filter(promotion_id=promotion_id, file_id=promotion_image_id).first()
        if img_obj:
            image = img_obj.url
        else:
            result = client.get_promotion_image(promotion_id, promotion_image_id)
            if result:
                new_img_obj = models.PromotionImage.objects.create(promotion_id=promotion_id, file_id=promotion_image_id, file_extension=result['file']['extension'])
                new_img_obj.save_file(result['filedata'].encode('utf-8'))
                new_img_obj.save()
                image = new_img_obj.url
    else:
        image = "/static/images/default-placeholder-image.webp"
    return image


AVAILABLE_PETS_CACHE_KEY = "get_available_pets:{pet_type_names}:breed_slugs:{breed_slugs}:locations:{locations}:"\
                           "status_id:{pet_status_id}:order_by:{order_by}:pet_with_images:{pet_with_images}:"\
                           "filters:{filters}:offset:{offset}:limit:{limit}"  # noqa
AVAILABLE_PETS_CACHE_TIMEOUT = 5 * 60


def get_available_pets(
    pet_type_names: Optional[Union[List[str], str]] = None,
    breed_slugs: Optional[Union[List[str], str]] = None,
    client: Optional[PWAPI] = None,
    location_ids: Optional[List[int]] = None,
    pet_status_id: Optional[str] = None,
    order_by: Optional[str] = None,
    pet_with_images: Optional[bool] = True,
    filters: Optional[Dict[str, Any]] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> Dict:
    if pet_type_names is not None:
        if not isinstance(pet_type_names, list):
            pet_type_names = [pet_type_names]
    
    if breed_slugs is not None:
        if not isinstance(breed_slugs, list):
            breed_slugs = [breed_slugs]
    breed_slugs_joined = ",".join(breed_slugs) if breed_slugs else None
    
    pet_type_names_joined = ",".join(pet_type_names) if pet_type_names else None
    location_joined = (
        ",".join(str(loc) for loc in location_ids) if location_ids else None
    )
    cache_key = AVAILABLE_PETS_CACHE_KEY.format(
        pet_type_names=pet_type_names_joined,
        breed_slugs=breed_slugs_joined,
        locations=location_joined,
        pet_status_id=pet_status_id,
        order_by=order_by,
        pet_with_images=pet_with_images,
        filters=filters,
        offset=offset,
        limit=limit,
    )
    result = cache.get(cache_key)

    if result is None:

        quippet_params = utils.get_base_quippet_params()
        
        if pet_with_images:
            quippet_params["qp_pet_has_image"] = True
        if pet_type_names_joined:
            quippet_params["qp_ptype_name"] = pet_type_names_joined
        if breed_slugs_joined:
            quippet_params["qp_pbrd_slug"] = breed_slugs_joined
        if location_joined:
            quippet_params["qp_pet_currently_at_entity_id"] = location_joined
        if pet_status_id:
            quippet_params["qp_pet_sub_status_id"] = pet_status_id
        if order_by:
            quippet_params["order_by"] = order_by
        if offset is not None:
            quippet_params["offset"] = offset
        if limit is not None:
            quippet_params["limit"] = limit
        if filters is not None:
            quippet_params.update(filters)

        result = client.get_pets(**dict(quippet_params=quippet_params))
        cache.set(cache_key, result, AVAILABLE_PETS_CACHE_TIMEOUT)

    return result

SIMILAR_PETS_CACHE_KEY = 'pinogy_carousel:utils:get_similar_pets:{breed_slug}_{location_ids}'
SIMILAR_PETS_CACHE_TIMEOUT = 5 * 60

def get_similar_pets(pet_type_slug: str, breed_slug: str, client: Optional[PWAPI] = None, locations: Optional[List[str]] = None) -> List[Dict]:
    cache_key = SIMILAR_PETS_CACHE_KEY.format(breed_slug=breed_slug, location_ids=locations)
    result = cache.get(cache_key)

    if result is None:
        if not client:
            client = PWAPI()
            
        kwargs = {
            "breed_slug": breed_slug,
            "location_ids": locations or [],
            "force_json": True
        }

        api_result = client.get_similar_pets(**kwargs)['objects']
        
        # Wrapping the result to same as /pet_search quippet
        result = []
        for pet in api_result:
            pet_images = utils.add_pet_image(
                client,
                [image["file"]["id"] for image in pet["images"]], pet.get("id")
            )
            wrapped_data = {
                'pet_id': pet["id"],
                'pet_name': pet["name"],
                "pet_gender": pet["gender"],
                "pbrd_display_name": pet["breed"]["display_name"],
                "loc_receipt_name": pet["location"]["entity"]["name"],
                "pet_type_id": pet["pet_type_id"],
                "ptype_slug": pet_type_slug,
                "pbrd_slug": pet["breed"]["slug"],
                "pet_images": pet_images
            }
            result.append(wrapped_data)

        cache.set(cache_key, result, SIMILAR_PETS_CACHE_TIMEOUT)

    return result

BREED_AVAILABLE_PETS_CACHE_KEY = 'pinogy_carousel:utils:get_breed_available_pets:{breed_slug}_{location_ids}'
BREED_AVAILABLE_PETS_CACHE_TIMEOUT = 5 * 60

def get_breed_available_pets(pet_type_slug: str, breed_slug: str, client: Optional[PWAPI] = None, locations: Optional[List[str]] = None) -> Dict:
    cache_key = BREED_AVAILABLE_PETS_CACHE_KEY.format(breed_slug=breed_slug, location_ids=locations)
    result = cache.get(cache_key)

    if result is None:
        if not client:
            client = PWAPI()
            
        kwargs = {
            "breed_slug": breed_slug,
            "show_other_if_missing": True,
            "location_ids": locations or [],
            "force_json": True
        }

        api_result = client.get_available_pets(
            **kwargs
        )['objects']
        
        # Wrapping the result to same as /pet_search quippet
        result = []
        for pet in api_result:
            pet_images = utils.add_pet_image(
                client,
                [image["file"]["id"] for image in pet["images"]], pet.get("id")
            )
            wrapped_data = {
                'pet_id': pet["id"],
                'pet_name': pet["name"],
                "pet_gender": pet["gender"],
                "pbrd_display_name": pet["breed"]["display_name"],
                "loc_receipt_name": pet["location"]["entity"]["name"],
                "pet_type_id": pet["pet_type_id"],
                "ptype_slug": pet_type_slug,
                "pbrd_slug": pet["breed"]["slug"],
                "pet_images": pet_images
            }
            result.append(wrapped_data)

        cache.set(cache_key, result, BREED_AVAILABLE_PETS_CACHE_TIMEOUT)

    return result