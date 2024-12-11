from django.core.management.base import BaseCommand
from django.db import transaction
from cmsplugin_cascade.models import CascadeElement
from pinogy_pet.models import PetListPluginModel
import json

class Command(BaseCommand):
    help = 'Updates PetlistPlugin instances with default data'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                # Fetch all records from CmspluginCascadeElement
                elements = CascadeElement.objects.filter(plugin_type='PetListPlugin').values().order_by("-cmsplugin_ptr_id")

                for element in elements:
                    id = int(element['id'])
                    placeholder_id = element['placeholder_id']
                    # CascadeElement.objects.filter(id=id).delete()
                    # PetDetailPluginModel.objects.filter(id=id).delete()     
                    button_data = {}    
                    counter = 1       
                    if element['glossary'].get('ask_about_me') == 'true':
                        button_data['btn'+str(counter)] = {}
                        button_data['btn'+str(counter)]['button_text'] = 'Ask About Me'
                        button_data['btn'+str(counter)]['button_selector'] = 'ask_about_me'
                        button_data['btn'+str(counter)]['button_style'] = element['glossary'].get('ask_about_me_button') or 'fill'
                        counter +=1

                    if element['glossary'].get('more_info') == 'true':
                        button_data['btn'+str(counter)] = {}
                        button_data['btn'+str(counter)]['button_text'] = 'More Info'
                        button_data['btn'+str(counter)]['button_selector'] = 'more_info'
                        button_data['btn'+str(counter)]['button_style'] = element['glossary'].get('more_info_button') or 'fill'
                        counter +=1

                    if element['glossary'].get('schedule_a_play_date') == 'true':
                        button_data['btn'+str(counter)] = {}
                        button_data['btn'+str(counter)]['button_text'] = 'Schedule a Play Date' 
                        button_data['btn'+str(counter)]['button_selector'] = 'schedule_a_playdate'
                        button_data['btn'+str(counter)]['button_style'] = element['glossary'].get('schedule_a_play_button') or 'fill'
                        counter +=1

                    if element['glossary'].get('call_now') == 'true':
                        button_data['btn'+str(counter)] = {}
                        button_data['btn'+str(counter)]['button_text'] = 'Call Now' 
                        button_data['btn'+str(counter)]['button_selector'] = 'call_now'
                        button_data['btn'+str(counter)]['button_style'] = element['glossary'].get('call_now_button') or 'fill'
                        counter +=1
                    CascadeElement.objects.filter(id=id).delete()
                    PetListPluginModel.objects.create(
                        glossary=element['glossary'],
                        button_data=button_data,
                        placeholder_id=placeholder_id,
                        plugin_type='PetListPlugin',
                        language='en'
                    )
                    print("ids",id)
            self.stdout.write(self.style.SUCCESS('Successfully updated PetDetailPlugin instances'))
        
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error occurred: {e}'))
            raise