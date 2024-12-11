from django.core.management.base import BaseCommand
from django.db import transaction
from cmsplugin_cascade.models import CascadeElement
from pinogy_breeds.models import BreedDetailPluginModel
import json

class Command(BaseCommand):
    help = 'Updates BreedDetailPlugin instances with default data'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                # Fetch all records from CmspluginCascadeElement
                breed_detail_elements = CascadeElement.objects.filter(plugin_type='BreedDetailPlugin').values().order_by("-cmsplugin_ptr_id")

                # delete existing breed traits and breed notes plugin 
                CascadeElement.objects.filter(plugin_type='BreedTraitsPlugin').delete()
                CascadeElement.objects.filter(plugin_type='BreedNotesPlugin').delete()

                default_glossary = {
                "message": "Want to know more about {breed_name} ?",
                "traits_layouts": "LAYOUT1",
                "show_breed_notes": "True",
                "show_breed_traits": "True",
                "breedform_button_style": "fill"
                }

                for element in breed_detail_elements:
                    id = element['id']
                    placeholder_id = element['placeholder_id']
                    CascadeElement.objects.filter(id=id).delete()
                    BreedDetailPluginModel.objects.filter(id=id).delete()
                    BreedDetailPluginModel.objects.create(
                        glossary=default_glossary,
                        placeholder_id=placeholder_id,
                        plugin_type='BreedDetailPlugin',
                        language='en'
                    )

            self.stdout.write(self.style.SUCCESS('Successfully updated BreedDetailPlugin instances'))
        
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error occurred: {e}'))
            raise