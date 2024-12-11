from django.core.management import BaseCommand
from cmsplugin_cascade.models import CascadeElement
from pos_api.pos_client import PWAPI
from pinogy_pet.utils import get_photos_meta, get_pet_filters
class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self,*args, **Options):
        value = CascadeElement.objects.filter(plugin_type = 'PetListPlugin').values().order_by("-cmsplugin_ptr_id")
        for data in value:
            glossary_data = data.get('glossary', {})
            if glossary_data.get("call_now"):
                glossary_data.update({"call_now" : "false"})
            if glossary_data.get("schedule_a_play_date"):
                glossary_data.update({"schedule_a_play_date" : "false"})
            if glossary_data.get("more_info"):
                glossary_data.update({"more_info" : "true"})
            if glossary_data.get("ask_about_me"):
                glossary_data.update({"ask_about_me" : "true"})

            # colors
            if glossary_data.get("call_now_button"):
                glossary_data.update({"call_now_button" : "fill"})
            if glossary_data.get("schedule_a_play_button"):
                glossary_data.update({"schedule_a_play_button" : "fill"})
            if glossary_data.get("ask_about_me_button"):
                glossary_data.update({"ask_about_me_button" : "fill"})
            if glossary_data.get("more_info_button"):
                glossary_data.update({"more_info_button" : "fill"})
            
            self.client = PWAPI()
            pet_status_list_=get_pet_filters(client=self.client,pet_type_name=None)
            pet_filter_list =[
                f'{pet_status["param"]}'
                for pet_status in pet_status_list_["filters"]
                if pet_status["enabled"] is True and pet_status['param'] != None
                ] 
            glossary_data.update({"pet_filter" : pet_filter_list})
            CascadeElement.objects.filter(id = data.get('id')).update(glossary = glossary_data)
        print("pet list plugin data updated...")
