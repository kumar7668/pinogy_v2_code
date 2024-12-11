from django.core.management.base import BaseCommand
from django.db import transaction
from cmsplugin_cascade.models import CascadeElement
from pinogy_pet.models import PetDetailPluginModel
import json

class Command(BaseCommand):
    help = 'Updates PetDetailPlugin instances with default data'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                # Fetch all records from CmspluginCascadeElement
                elements = CascadeElement.objects.filter(plugin_type='PetDetailPlugin').values().order_by("-cmsplugin_ptr_id")

                default_btn_data = {
                            "btn1": {
                                "button_top": "true",
                                "button_link": "",
                                "button_text": "Call Now",
                                "button_style": "outline",
                                "button_width": "false",
                                "button_selector": "call_now",
                                "internallink_id": "",
                                "id_button_target": "_self",
                                "link_choice_field": "Internal link",
                                "button_color_pattern": "O2",
                                "id_button_internallink": ""
                            },
                            "btn2": {
                                "button_top": "false",
                                "button_link": "",
                                "button_text": "Ask About Me",
                                "button_style": "outline",
                                "button_width": "true",
                                "button_selector": "ask_about_me",
                                "internallink_id": "",
                                "id_button_target": "_self",
                                "link_choice_field": "Internal link",
                                "button_color_pattern": "O2",
                                "id_button_internallink": ""
                            },
                            "btn3": {
                                "button_top": "false",
                                "button_link": "",
                                "button_text": "Schedule a Playdate",
                                "button_style": "fill",
                                "button_width": "true",
                                "button_selector": "schedule_a_playdate",
                                "internallink_id": "",
                                "id_button_target": "_self",
                                "link_choice_field": "Internal link",
                                "button_color_pattern": "F2",
                                "id_button_internallink": ""
                            }
                            }

                default_glossary = {
                    "message": "Ask about {pet_name} ?",
                    "pet_detail": [],
                    "button_type": "",
                    "promotion_banner": "false",
                    "button_selector_1": "ask_about_me",
                    "button_settings_1": "",
                    "first_button_link": "",
                    "first_button_text": "",
                    "first_button_style": "",
                    "btn_type_link_choice": "External link",
                    "petform_button_style": "fill",
                    "alt_name_promob_image": "",
                    "button_internallink_1": {
                        "pk": 57,
                        "model": "cms.page"
                    },
                    "consumer_verification": "false",
                    "btn_type_external_link": "http://www.google.com",
                    "btn_type_internal_link": {
                        "pk": 6,
                        "model": "cms.page"
                    },
                    "link_choice_field_btn1": "",
                    "first_button_fill_color": "",
                    "first_button_font_color": "",
                    "first_button_color_pattern": "",
                    "first_button_outline_color": ""
                }

                for element in elements:
                    id = element['id']
                    placeholder_id = element['placeholder_id']
                    CascadeElement.objects.filter(id=id).delete()
                    PetDetailPluginModel.objects.filter(id=id).delete()
                    PetDetailPluginModel.objects.create(
                        glossary=default_glossary,
                        button_data=default_btn_data,
                        placeholder_id=placeholder_id,
                        plugin_type='PetDetailPlugin',
                        language='en'
                    )

            self.stdout.write(self.style.SUCCESS('Successfully updated PetDetailPlugin instances'))
        
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error occurred: {e}'))
            raise