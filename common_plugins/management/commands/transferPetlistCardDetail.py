from django.core.management import BaseCommand
from cmsplugin_cascade.models import CascadeElement
from pos_api.pos_client import PWAPI
from pinogy_pet.utils import get_photos_meta, get_pet_filters
from pinogy_pet.pos_api import PetTypeSetting
class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self,*args, **Options):
        PET_DETAIL=["status","normal_price_list","location",
                    "petname","breedername", "birthdate","sex",
                    "age","usda","Breeder_Info","badges"
        ]

        pet_setting = PetTypeSetting()
       
        value = CascadeElement.objects.filter(plugin_type = 'PetListPlugin').values().order_by("-cmsplugin_ptr_id")
        for atr in PET_DETAIL:
            if hasattr(pet_setting, atr[0]):
                if not getattr(pet_setting, atr[0]):
                    PET_DETAIL.remove(atr)
            else:
                PET_DETAIL.remove(atr)
        for data in value:
            glossary_data = data.get('glossary', {})
            glossary_data.update({"pet_detail" : PET_DETAIL})
            CascadeElement.objects.filter(id = data.get('id')).update(glossary = glossary_data)
        print("pet list plugin data updated...")
