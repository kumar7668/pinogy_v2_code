from django.core.management import BaseCommand
from cms.models import Page
from common_plugins.models import BannerPluginModel


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self,*args, **Options):
        value = BannerPluginModel.objects.values()
        for data in value:
            mydict = {} 
            glossary_data = data.get('glossary', {})
            
            if glossary_data.get('first_button_text'):
                mydict['btn1'] = {}
                mydict['btn1']['button_text'] = glossary_data.get('first_button_text') or ''
                mydict['btn1']['button_style'] =glossary_data.get('first_button_style') or '' 
                mydict['btn1']['id_button_target'] =glossary_data.get('first_button_target') or ''
                if glossary_data.get('first_button_internallink'):
                    if Page.objects.filter(id = glossary_data.get('first_button_internallink').get('pk')).exists():
                        mydict['btn1']['internallink_id'] = glossary_data.get('first_button_internallink').get('pk') or ''
                        page = Page.objects.get(id = glossary_data.get('first_button_internallink').get('pk'))
                        mydict['btn1']['id_button_internallink'] = page.get_absolute_url() or ''
                mydict['btn1']['button_color_pattern'] =glossary_data.get('first_button_color_pattern') or '' 
                mydict['btn1']['button_phone_link'] =glossary_data.get('first_button_phone_link') or ''
                mydict['btn1']['link_choice_field'] =glossary_data.get('link_choice_field_btn1') or 'Internal link'
                mydict['btn1']['button_link'] =glossary_data.get('first_button_link') or '' 
            
            if glossary_data.get('second_button_text') and glossary_data.get('second_button_text') not in ["Second Btn", "Click Here"] and glossary_data.get('second_button_link') != "" and glossary_data.get('second_button_internallink') != None:
                mydict['btn2'] = {}
                mydict['btn2']['button_text'] =glossary_data.get('second_button_text') or '' 
                mydict['btn2']['button_style'] =glossary_data.get('second_button_style') or ''
                mydict['btn2']['id_button_target'] =glossary_data.get('second_button_target') or ''
                if glossary_data.get('second_button_internallink'):
                    if Page.objects.filter(id = glossary_data.get('second_button_internallink').get('pk')).exists():
                        mydict['btn2']['internallink_id'] = glossary_data.get('second_button_internallink').get('pk')
                        page = Page.objects.get(id = glossary_data.get('second_button_internallink').get('pk'))
                        mydict['btn2']['id_button_internallink'] = page.get_absolute_url() or ''
                mydict['btn2']['button_color_pattern'] =glossary_data.get('second_button_color_pattern') or ''
                mydict['btn2']['button_phone_link'] =glossary_data.get('second_button_phone_link') or '' 
                mydict['btn2']['link_choice_field'] =glossary_data.get('link_choice_field_btn2') or 'Internal link' 
                mydict['btn2']['button_link'] =glossary_data.get('second_button_link') or ''

            BannerPluginModel.objects.filter(id = data['id']).update(button_data = mydict)
        print("banner plugin (buttons) fields data transfered to json field button_data")
