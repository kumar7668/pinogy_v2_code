from django.core.management import BaseCommand
from cms.models import Page
from common_plugins.models import FooterPluginModel


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self,*args, **Options):
        value = FooterPluginModel.objects.values()
        for data in value:
            glossary_data = data.get('glossary', {})
            if glossary_data:
                queryset=Page.objects.filter(publisher_is_draft=True)
                # queryset=Page.objects.filter(publisher_is_draft=True,title_set__publisher_state = 0,in_navigation = True)
                quick_links_data = [
                query.id for query in queryset if query.in_navigation and query.parent_page == None]
                glossary_data['quick_links'] = quick_links_data
                FooterPluginModel.objects.filter(id = data['id']).update(glossary = glossary_data)
            elif glossary_data['quick_links'] == []:
                queryset=Page.objects.filter(publisher_is_draft=True)
                quick_links_data = [
                query.id for query in queryset if query.in_navigation and query.parent_page == None]
                glossary_data['quick_links'] = quick_links_data
                FooterPluginModel.objects.filter(id = data['id']).update(glossary = glossary_data)
        print("footer plugin (buttons) fields data transfered to json field button_data")




