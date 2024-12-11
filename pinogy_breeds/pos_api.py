from typing import List, Dict, Optional
from dataclasses import dataclass, field
from django.core.cache import cache

from pos_api.pos_client import PWAPI
from pinogy_breeds.models import ApiBreedPhoto, ApiBreedBadgePhoto
from pinogy_breeds import utils

BREEDS_LIST_WITH_IMAGES_CACHE_KEY = 'pinogy_breeds:pos_api:BreedList:get_breeds_list:{ptype_slug}:{ptypes_ids}'
BREEDS_LIST_WITH_IMAGES_CACHE_TIMEOUT = 60 * 60
BREEDS_DETAIL_WITH_IMAGES_CACHE_KEY = 'pinogy_breeds:pos_api:BreedDetail:get_breeds_detail:{brd_slug}'
BREEDS_DETAIL_WITH_IMAGES_CACHE_TIMEOUT = 60 * 60
BREEDS_API_DETAIL_CACHE_KEY = 'pinogy_breeds:pos_api:BreedDetail:_get_api_breeds_data:{brd_slug}'
BREEDS_API_DETAIL_CACHE_TIMEOUT = 60 * 60
PET_TYPE_LIST_CACHE_KEY = 'pinogy_breeds:pos_api:get_pet_type_list:{ptypes_ids}'
PET_TYPE_LIST_CACHE_TIMEOUT = 60 * 60 * 24

@dataclass
class PetType:
    id: str
    name: str
    slug: str
    plurals: Dict[str, str]
    selected_plural: str

@dataclass
class BreedMetric:
    id: str
    name: str
    value: int

@dataclass
class BreedNote:
    id: str
    header: str
    description: str
    sort: int
    group_id: int
    group_name: str
    

@dataclass
class Breed:
    id: str
    name: str
    slug: str
    description: Optional[str]
    custom_fields: Dict[str, str]
    notes: Dict[str, List[BreedNote]] = field(default_factory=dict)
    metrics: List[BreedMetric] = field(default_factory=list)
    images: List[Dict[str, any]] = field(default_factory=list)
    badge_images: List[Dict[str, any]] = field(default_factory=list)
    pet_type: Optional[PetType] = None

class PetTypeMixin(object):
    
    def get_pet_type_object(self, pet_type_data: Dict[str, any]) -> PetType:
            
            name = pet_type_data['name']
            selected_plural = pet_type_data.get('plurals').get(name, name) if pet_type_data.get('plurals') else name 

            return PetType(
                id=pet_type_data['id'],
                name=name,
                slug=pet_type_data['slug'],
                plurals=pet_type_data['plurals'],
                selected_plural = selected_plural,
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
    
    def _get_breed_metrics(self, breed_metrics: Dict[str, any]) -> List[BreedMetric]:
        
        breed_metrics_objects = []
        for metric in breed_metrics:
            if metric["deleted"]:            
                continue

            metric_obj = BreedMetric(
                id=metric.get('id'),
                name=metric.get('name'),
                value=int(metric.get('value')),
            )
            breed_metrics_objects.append(metric_obj)
        
        return breed_metrics_objects

    def _get_breed_notes(self, breed_notes: Dict[str, any]) -> Dict[str, List[BreedNote]]:
        
        breed_notes_groups = {}
        for note in breed_notes:
            if note["deleted"]:            
                continue
            
            if note['group'] is not None:
              group_name = note['group']['name']
              group_id = note['group']['id']
              
            note_obj = BreedNote(
                id=note['id'],
                header=note['header'],
                description=note['description'],
                sort=note['sort_index'],
                group_id=group_id,
                group_name=group_name,  
            )
            
            if breed_notes_groups.get(group_name, None):
                breed_notes_groups[group_name].append(note_obj)
            else:
                breed_notes_groups[group_name] = [note_obj]
        
        if breed_notes_groups:
            for breed_group_name ,breed_group in breed_notes_groups.items():
                breed_notes_groups[breed_group_name] = sorted(breed_group, key=lambda breed_group: breed_group.sort)
        
        return breed_notes_groups
    
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

        breed_images = ApiBreedPhoto.objects.get_images(
            client=client,
            api_images_data=api_breed_images,
            model_filters={"breed_id": breed_id},
            non_defaults={"breed_id": breed_id}
        )

        return breed_images

    def _get_breed_badge_images(self, client: PWAPI,  api_badge_images: List[Dict[str, any]]) -> List[Dict[str, any]]:

        breed_badges = ApiBreedBadgePhoto.objects.get_images(
            client=client, 
            api_images_data=api_badge_images, 
            model_defaults={"height": 76, "width": 76}, 
            default_image=False
        )

        return breed_badges

class BreedList(BreedMixin):
    """
    Fetch data from POS and work around it
    """
    
    def __init__(self):
        self.client = PWAPI()
    
    def get_breed_list(self, 
        pet_type_slug: Optional[str] = None, 
        pet_type_ids: Optional[List[str]] = None
    ) -> List[Dict[str, any]]:
        
        cache_key = BREEDS_LIST_WITH_IMAGES_CACHE_KEY.format(
            ptype_slug=pet_type_slug,
            ptypes_ids=pet_type_ids
        )
        
        if result := cache.get(cache_key):
            return result
        
        breed_data = self._get_api_breeds_list(pet_type_slug=pet_type_slug, pet_type_ids=pet_type_ids)
    
        breed_list = []
        for breed in breed_data:
            breed_obj = self._get_breed_list_object(breed)
            breed_images = self._get_breed_images(self.client, breed['id'], breed['images'])
            breed_obj.images = breed_images
            breed_list.append(breed_obj)
        
        cache.set(cache_key, breed_list, BREEDS_LIST_WITH_IMAGES_CACHE_TIMEOUT)
        return breed_list
    
class BreedDetail(BreedMixin):
    """
    Fetch breed data from POS and work around it
    """
    
    def __init__(self):
        self.client = PWAPI()

    def _get_api_breeds_data(
        self,
        breed_slug: str,
        client: Optional[PWAPI] = None,
    ) -> Dict:
        
        cache_key = BREEDS_API_DETAIL_CACHE_KEY.format(
            brd_slug=breed_slug
        )
        
        if result := cache.get(cache_key):
            return result
        
        if not client:
            client = PWAPI()
            
        result = client.get_breed(slug=breed_slug)
        cache.set(cache_key, result, BREEDS_API_DETAIL_CACHE_TIMEOUT)

        return result
    
    def get_breed_data(self, 
        breed_slug: str, 
    ) -> Breed:
        
        cache_key = BREEDS_DETAIL_WITH_IMAGES_CACHE_KEY.format(
            brd_slug=breed_slug
        )
        
        if result := cache.get(cache_key):
            return result
        
        breed_data = self._get_api_breeds_data(breed_slug=breed_slug)
        
        breed_obj = self._get_breed_list_object(breed_data)
        
        breed_images = self._get_breed_images(self.client, breed_data['id'], breed_data['images'])
        breed_obj.images = breed_images
        
        badge_images = self._get_breed_badge_images(self.client, breed_data['badges'])
        breed_obj.badge_images = badge_images
        
        breed_obj.metrics = self._get_breed_metrics(breed_data['metrics'])
        
        breed_obj.notes = self._get_breed_notes(breed_data['notes'])

        cache.set(cache_key, breed_obj, BREEDS_DETAIL_WITH_IMAGES_CACHE_TIMEOUT)
        return breed_obj

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