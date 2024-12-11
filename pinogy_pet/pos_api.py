import ast

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from django.core.cache import cache

from pos_api.pos_client import PWAPI
from pinogy_pet.models import ApiPetTypePhoto
from pinogy_breeds import utils

BREEDS_LIST_WITH_IMAGES_CACHE_KEY = 'pinogy_pet:pos_api:BreedList:get_breeds_list:{ptypes_ids}'
BREEDS_LIST_WITH_IMAGES_CACHE_TIMEOUT = 60 * 60
PET_TYPE_LIST_CACHE_KEY = 'pinogy_pet:pos_api:get_pet_type_list:{ptypes_ids}'
PET_TYPE_LIST_CACHE_TIMEOUT = 60 * 60 * 24
SETTINGS_FOR_PET_TYPE_CACHE_KEY = 'pinogy_pet:pos_api:_get_api_pet_type_setting:{pet_type_id}'
SETTINGS_FOR_PET_TYPE_CACHE_TIMEOUT = 60 * 60

# PRICE OPTION CONSTANT
SALE_PRICE = "Sale Price, Else Price"  # Display sale price else normal price in both listing and detail page
ONLY_SALE_PRICE = "Sale Prices Only" # Display only sale price in both listing and detail page
NO_PRICE = "No Prices" # Do not display price
SALE_PRICE_DETAILS = "Sale Price, Else Price (Detail Pages Only)"  # Display sale price else normal price only in detail page
ONLY_SALE_PRICE_DETAILS = "Sale Prices Only (Detail Pages Only)" # Display only sale price only in detail page

@dataclass
class PetType:
    id: str
    name: str
    slug: str
    plurals: Dict[str, str]

@dataclass
class Breed:
    id: str
    name: str
    slug: str
    description: Optional[str]
    custom_fields: Dict[str, str]
    images: List[Dict[str, any]] = field(default_factory=list)
    pet_type: Optional[PetType] = None

class PetTypeMixin(object):
    
    def get_pet_type_object(self, pet_type_data: Dict[str, any]) -> PetType:
        return PetType(
            id=pet_type_data['id'],
            name=pet_type_data['name'],
            slug=pet_type_data['slug'],
            plurals=pet_type_data['plurals']
        )
    
    def _get_api_pet_type_list(self, client: Optional[PWAPI] = None) -> List[Dict]:
        if client is None:
            client = PWAPI()
            
        return client.get_pet_types()['objects']

class BreedMixin(object):
    
    def _get_breed_list_object(self, breed_data: Dict[str, any]) -> Breed:
        pet_type_mixin = PetTypeMixin()
        pet_type_obj = pet_type_mixin.get_pet_type_object(breed_data.get('pet_type'))
        
        return Breed(
            id=breed_data.get('id'),
            name=breed_data.get('display_name'),
            slug=breed_data.get('slug'),
            description=breed_data.get('description'),
            custom_fields=breed_data.get('custom_fields'),
            pet_type=pet_type_obj
        )
    
    def _get_api_breeds_list(
        self,
        pet_type_slug: Optional[str] = None,
        client: Optional[PWAPI] = None,
        available_only: bool = False,
        # pet_location_ids: Optional[List[int]] = None,
        pet_type_ids: Optional[List[int]] = None,
        search_val= None
    ) -> Dict:
        
        if not client:
            client = PWAPI()

        kwargs = {'to_be_displayed': True}

        #TODO: need to update key
        # if pet_location_id:
        #     kwargs['to_be_displayed'] = {"location_ids": pet_location_id}

        for key, value in (
            ('pet_type_slug', pet_type_slug),
            # ('pet_location_id', pet_location_id),
            ('pet_type_id', pet_type_ids),
        ):
            if value:
                kwargs[key] = value

        if available_only:
            kwargs['pet_status_id'] = -1
        
        if search_val:
            kwargs['display_name_like'] = search_val

        #TODO: Handle exceptions here
        result = client.get_breeds(**kwargs)['objects']
        
        return result
        
  
    def _get_breed_images(self, client: PWAPI,  breed_id: int, api_breed_images: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """
        Get breed images
            1. get images from database
            2. check with pos images if any image is missing in DB than fetch that image from POS and save it in db
            3. create a list of dict which contains image_url and sort order
            4. return sorted images based on sort_order

        Args:
            client (PWAPI): PWAPI object
            breed_id (int): breed id
            api_breed_images (List[Dict[str, any]]): list of breed images 

        Returns:
            List[Dict[str, any]]: return list of image urls
        """
        
        if not api_breed_images:
            return [{
                'sort_order': 0,
                'image_url': '/static/images/default-placeholder-image.webp'
            }]
        
        available_breed_images = ApiBreedPhoto.objects.filter(breed_id=breed_id)
        breed_photo_set = {breed_image.file_id : breed_image for breed_image in available_breed_images}
        
        breed_images = []
        for image in api_breed_images:
            breed_image = {
                "sort_order": image['sort_order']
            }
            
            if image['file']['id'] in breed_photo_set:
                breed_image["image_url"] = breed_photo_set[image['file']['id']].url
            else:
                api_breed_image = self._get_breed_image_from_api(client, breed_id, image['file']['id'])
                if api_breed_images is None: 
                    continue
                breed_image["image_url"] = api_breed_image.url
            
            breed_images.append(breed_image)
        return sorted(breed_images, key=lambda image: image['sort_order'])

class BreedList(BreedMixin):
    """
    Fetch data from POS and work around it
    """
    
    def __init__(self):
        self.client = PWAPI()
    
    def get_breed_list(self, pet_type_ids: Optional[List[str]] = None) -> List[Dict[str, any]]:
        
        cache_key = BREEDS_LIST_WITH_IMAGES_CACHE_KEY.format(
            ptypes_ids=pet_type_ids
        )
        
        if result := cache.get(cache_key):
            return result
        
        breed_data = self._get_api_breeds_list(pet_type_ids=pet_type_ids)
    
        breed_list = []
        for breed in breed_data:
            breed_obj = self._get_breed_list_object(breed)
            breed_images = self._get_breed_images(self.client, breed['id'], breed['images'])
            breed_obj.images = breed_images
            breed_list.append(breed_obj)
        
        cache.set(cache_key, breed_list, BREEDS_LIST_WITH_IMAGES_CACHE_TIMEOUT)
        return breed_list  

class PetTypeList(PetTypeMixin):
    """
    Fetch data from POS and work around it
    """

    def __init__(self):
        self.client = PWAPI()
    
    def get_pet_type_list(self, pet_type_ids: Optional[List[str]] = None) -> List[PetType]:
        
        cache_key = PET_TYPE_LIST_CACHE_KEY.format(
            ptypes_ids=str(pet_type_ids) if pet_type_ids else ''
        )
        
        if result := cache.get(cache_key):
            return result
        
        pet_type_data = self._get_api_pet_type_list()
    
        pet_type_list = []
        for pet_type in pet_type_data:
            if not pet_type['is_enabled'] or pet_type['deleted']:
                continue
            
            if pet_type_ids and str(pet_type['id']) not in pet_type_ids:
                continue
                
            pet_type_obj = self.get_pet_type_object(pet_type)
            pet_type_list.append(pet_type_obj)
        
        cache.set(cache_key, pet_type_list, PET_TYPE_LIST_CACHE_TIMEOUT)
        return pet_type_list

    def get_pet_type_photo(self, pet_type_id, pet_type_name):
        # Check API pet type photo from Pinogy API
        try:
            client = PWAPI()
            api_img = client.get_pet_type_image(pet_type_id)['objects']
            # If photo exist
            if api_img:
                # Check if pet type photo in DB
                pet_type_photo_obj = ApiPetTypePhoto.objects.filter(pet_type_id=pet_type_id).first()
                if pet_type_photo_obj:
                    # Compare id pet type photo from DB and API
                    if pet_type_photo_obj.file_id != api_img[0]['image']['file']['id']:
                        # If photo id's are different, first remove the photo from the DB
                        pet_type_photo_obj.delete()
                        # Load photo from API
                        img_load = client.get_file([api_img[0]['image']['file']['id']])['objects'][0]
                        file_data = img_load['flin_contents'].encode('utf-8')
                        pet_type_photo_obj = ApiPetTypePhoto.objects.create(
                            pet_type_id=pet_type_id,
                            file_extension='jpeg',
                            file_id=api_img[0]['image']['file']['id'],
                        )
                        pet_type_photo_obj.save_file(file_data)
                else:
                    # If Pet Type Photo doesn't store in DB load from API
                    img_load = client.get_file([api_img[0]['image']['file']['id']])['objects'][0]
                    file_data = img_load['flin_contents'].encode('utf-8')
                    pet_type_photo_obj = ApiPetTypePhoto.objects.create(
                        pet_type_id=pet_type_id, file_extension='jpeg', file_id = api_img[0]['image']['file']['id']
                    )
                    pet_type_photo_obj.save()
                    pet_type_photo_obj.save_file(file_data)
                # And return url path pet type image
                return pet_type_photo_obj.file_image
            else:
                # The case when the API does not have a pet type photo, then call pets with same pet type name and order by img
                qp = dict(qp_ptype_name=pet_type_name, order_by='pet_has_images DESC', limit=20)
                pets = client.get_pets(quippet_params=qp)['pets']
                for pet in pets:
                    # Check if Pet have images
                    if pet['ptim_imgfile_file_ids']:
                        for pet_photo in pet['ptim_imgfile_file_ids']:
                            result = client.get_file([pet_photo])
                            if result['objects']:
                                img_load = result['objects'][0]
                                # Check photo extension and load
                                if img_load['file_orig_extension'] in ['jpg', 'png', 'gif', 'jpeg']:
                                    file_data = img_load['flin_contents'].encode('utf-8')
                                    pet_type_photo_obj = ApiPetTypePhoto.objects.create(
                                        pet_type_id=pet_type_id,
                                        file_extension=img_load['file_orig_extension'],
                                        file_id=pet_photo,
                                    )
                                    pet_type_photo_obj.save_file(file_data)
                                    return  pet_type_photo_obj.file_image
                return None
        except Exception as e:
                    print(e)
            
@dataclass
class VisibilitySettings:
    visible: bool = False
    visible_detail_only: bool = False
    visible_verification: bool = False
    visible_verification_detail_only: bool = False

    def __init__(self, setting: str="Hidden"):
        if setting == "Visible":
            self.visible = True
            self.visible_detail_only = True
        elif setting == "Visible (Detail Pages Only)":
            self.visible_detail_only = True
        elif setting == "Visible with Verification":
            self.visible_verification = True
            self.visible_verification_detail_only = True
        elif setting == "Visible with Verification (Detail Pages Only)":
            self.visible_verification_detail_only = True
    

# TODO: Need To Add action button and confirm the api response
@dataclass
class PetTypeSetting:
    pet_type_id: int = 0
    sex: VisibilitySettings = field(default_factory=VisibilitySettings)
    storecitystate: VisibilitySettings = field(default_factory=VisibilitySettings)
    storephone: VisibilitySettings = field(default_factory=VisibilitySettings)   
    usda: VisibilitySettings = field(default_factory=VisibilitySettings)
    aphis: VisibilitySettings = field(default_factory=VisibilitySettings)
    breedername: VisibilitySettings = field(default_factory=VisibilitySettings)
    breedercitystate: VisibilitySettings = field(default_factory=VisibilitySettings)
    petid: VisibilitySettings = field(default_factory=VisibilitySettings)
    petname: VisibilitySettings = field(default_factory=VisibilitySettings)
    birthdate: VisibilitySettings = field(default_factory=VisibilitySettings)
    petmarketingtext: VisibilitySettings = field(default_factory=VisibilitySettings)
    sale_price_list: bool = False
    normal_price_list: bool = False
    sale_price_detail: bool = False
    normal_price_detail: bool = False
class APIPetTypeSetting:
    
    def __init__(self):
        self.client = PWAPI()
    
    def _get_api_pet_type_setting(self, pet_type_id: int) -> List[Dict[str, any]]:
        result = self.client.cache_post_queries(**{
            "quippet_name": 'read__tbl__pet_settings',
            "quippet_params": {
                'qp_pstn_pet_type_id': pet_type_id,
                'qp_pstn_name': 'web.options.pettypes'
            }
        })['objects']
        
        return result

    def get_pet_type_setting_obj(self, pet_type_id: int) -> PetTypeSetting:
        cache_key = SETTINGS_FOR_PET_TYPE_CACHE_KEY.format(pet_type_id=str(pet_type_id))
        if result := cache.get(cache_key):
            return result

        pos_integration_data = self.client.get_website_data()
        setting = self.client.get_websites_setting(pos_integration_data.get('id')).get('pet_type_web_options')

        if not setting:
            result = PetTypeSetting(pet_type_id=0)
            cache.set(cache_key, result, SETTINGS_FOR_PET_TYPE_CACHE_TIMEOUT)
            return result

        setting=[item for item in setting if item['pet_type_id'] ==pet_type_id]
        if len(setting)==0:
            # make all setting off if data not set in POS
            setting={} 
        else:
            setting=setting[0]
        
        result = PetTypeSetting(
            pet_type_id=pet_type_id,
            sex=VisibilitySettings(setting["pet_gender"] if "pet_gender" in setting else ''),
            storecitystate=VisibilitySettings(setting["store_city_and_state"] if "store_city_and_state" in setting else ''),
            storephone=VisibilitySettings(setting["store_phone"] if "store_phone" in setting else ''),
            usda=VisibilitySettings(setting["usda_number"] if "usda_number" in setting else ''),
            aphis=VisibilitySettings(setting["usda_search_link"] if "usda_search_link" in setting else ''),
            breedername=VisibilitySettings(setting["breeder_name"] if "breeder_name" in setting else ''),
            breedercitystate=VisibilitySettings(setting["breeder_city_and_state"] if "breeder_city_and_state" in setting else ''),
            petid=VisibilitySettings(setting["pet_number"] if "pet_number" in setting else ''),
            petname=VisibilitySettings(setting["pet_name"] if "pet_name" in setting else ''),
            birthdate=VisibilitySettings(setting["pet_birth_date"] if "pet_birth_date" in setting else ''),
            petmarketingtext=VisibilitySettings(setting["marketing_text"] if "marketing_text" in setting else ''),
            sale_price_list="pet_price" in setting and setting["pet_price"] in [SALE_PRICE, ONLY_SALE_PRICE],
            normal_price_list="pet_price" in setting and setting["pet_price"] == SALE_PRICE,
            sale_price_detail="pet_price" in setting and setting["pet_price"] in [SALE_PRICE, ONLY_SALE_PRICE, SALE_PRICE_DETAILS, ONLY_SALE_PRICE_DETAILS],
            normal_price_detail="pet_price" in setting and setting["pet_price"] in [SALE_PRICE, SALE_PRICE_DETAILS],
        )
        
        cache.set(cache_key, result, SETTINGS_FOR_PET_TYPE_CACHE_TIMEOUT)
        return result