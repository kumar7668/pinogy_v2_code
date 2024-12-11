
from django.core.management import BaseCommand
from cms.models import Page
from common_plugins.models import SubscribePluginModel
from filer.models import File
class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self,*args, **Options):
        value = SubscribePluginModel.objects.all()
        for glossary_data in value:

            # if glossary_data.glossary['title']:
            title = glossary_data.glossary['title'] or ''
            subtitle = glossary_data.glossary['sub_title'] or ''
            glossary_data.glossary['marketing_message'] = '<h2 style = "font-size:40px">{0}</h2><h3 class = "h3-theme-bold subscribe_subtitle">{1}</h3>'.format(title,subtitle)

            if glossary_data.glossary['bg_image']:
                old_path = File.objects.get(id = glossary_data.glossary['bg_image']['pk']).file
                glossary_data.glossary['background'] = 'yes'
                glossary_data.glossary['background_type'] = 'Image'
                glossary_data.newsletter_bg_image = old_path
            else:
                # glossary_data.glossary['background'] = 'no'
                pass
              
            if glossary_data.glossary['display_text_left'] == False and glossary_data.glossary['side_image']:
                side_image = File.objects.get(id = glossary_data.glossary['side_image']['pk']).file
                glossary_data.glossary['marketing_layouts_email'] = 'LAYOUT4'
                glossary_data.newsletter_image = side_image
            elif glossary_data.glossary['display_text_left'] == False and glossary_data.glossary['display_default_image'] == True:
                glossary_data.glossary['marketing_layouts_email'] = 'LAYOUT4'
                glossary_data.glossary['background'] = 'yes'
                glossary_data.glossary['background_type'] = 'Color'
                glossary_data.glossary['bg_color'] = '#F3F4F6'

            else:
                glossary_data.glossary['marketing_layouts_email'] = 'LAYOUT1'
            glossary_data.glossary['marketing_button_text'] = 'Submit'
            glossary_data.glossary['marketing_button_style'] = 'fill'
            glossary_data.glossary['marketing_button_color'] = 'F2'
            glossary_data.glossary['marketing_list'] = 'Email'
            glossary_data.save()
        print("newsletter plugin fields data transfered to json field button_data")

