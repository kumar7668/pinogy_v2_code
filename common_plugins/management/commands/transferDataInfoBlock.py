from django.core.management import BaseCommand
from cms.models import Page
from common_plugins.models import InfoBlockFirstPluginModel
from custom_design.models import ThemeConfiguration

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self,*args, **Options):
        value = InfoBlockFirstPluginModel.objects.order_by("-id").values()
        assign_value_left = ['LAYOUT1', "LAYOUT3", "LAYOUT7"]
        assign_value_right = ['LAYOUT2', "LAYOUT4", "LAYOUT5"]
        for data in value:
            mydict = {} 
            glossary_data = data.get('glossary', {})
            if glossary_data.get('button_text'):
                mydict['btn1'] = {}
                mydict['btn1']['button_text'] = glossary_data.get('button_text', '')
                mydict['btn1']['button_style'] =glossary_data.get('button_style', '')  
                mydict['btn1']['id_button_target'] =glossary_data.get('button_target', '')
                if glossary_data.get('button_internallink'):
                    if Page.objects.filter(id = glossary_data.get('button_internallink').get('pk')).exists():
                        mydict['btn1']['internallink_id'] = glossary_data.get('button_internallink').get('pk', '') 
                        page = Page.objects.get(id = glossary_data.get('button_internallink').get('pk', ''))
                        mydict['btn1']['id_button_internallink'] = page.get_absolute_url() or ''
                mydict['btn1']['button_color_pattern'] = ThemeConfiguration.objects.last().secondary_button_color_pattern
                mydict['btn1']['button_phone_link'] = ''
                mydict['btn1']['link_choice_field'] =glossary_data.get('link_choice_field_btn1', 'Internal link') 
                mydict['btn1']['button_link'] =glossary_data.get('first_button_link') or '' 

            if data.get('video'):
                layout = glossary_data.get('layout')
                if layout in assign_value_left:
                    media_type = "Video"
                    video_type = 'upload'
                    layout_video = "LAYOUT13"
                    glossary_data.update({"media_type" : media_type, "video_type" : video_type, "layout_video" : layout_video, 'layout2' : 'LAYOUT12'})
                elif layout in assign_value_right:
                    media_type = "Video"
                    video_type = 'upload'
                    layout_video = "LAYOUT14"
                    glossary_data.update({"media_type" : media_type, "video_type" : video_type, "layout_video" : layout_video, 'layout2' : 'LAYOUT12'})
                InfoBlockFirstPluginModel.objects.filter(id = data['id']).update(glossary = glossary_data, button_data = mydict)

            elif data.get('image'):
                media_type = "Image"
                quantity_of_image = 'QTY1'
                glossary_data.update({"media_type" : media_type, "quantity_of_image" : quantity_of_image, 'layout2' : 'LAYOUT12'})
                InfoBlockFirstPluginModel.objects.filter(id = data['id']).update(glossary = glossary_data, button_data = mydict)
            
            else:
                glossary_data.update({'layout2' : 'LAYOUT12'})
                InfoBlockFirstPluginModel.objects.filter(id = data['id']).update(glossary = glossary_data, button_data = mydict)
    
        print("banner plugin (buttons) fields data transfered to json field button_data")
