from django.core.management import BaseCommand
from cms.models import Page
from common_plugins.models import HeaderPluginModel


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self,*args, **Options):
        value = HeaderPluginModel.objects.values()
        links_excluded_data = Page.objects.filter(publisher_is_draft=True,in_navigation = True,title_set__publisher_state = 0)
        quick_links_data = [
            str(query.id)
         for query in links_excluded_data ]

        for data in value:
            glossary_data = data.get('glossary', {})
            if glossary_data:
                glossary_data['custom_menus'] = quick_links_data
            HeaderPluginModel.objects.filter(id = data['id']).update(glossary = glossary_data)
        print("Header plugin (menus) : the available menus in header section will be checked on plugin ")
