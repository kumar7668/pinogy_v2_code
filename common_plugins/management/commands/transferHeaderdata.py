from django.core.management import BaseCommand
from cms.models import Page
from common_plugins.models import HeaderPluginModel


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self,*args, **Options):
        value = HeaderPluginModel.objects.values()

        queryset = Page.objects.filter(publisher_is_draft=True, in_navigation=False)
        descendant_ids = []
        for page in queryset:
            if page.is_home != True:
                descendants = page.get_descendant_pages()
                descendant_ids.extend(descendant.id for descendant in descendants)

        links_excluded_data = Page.objects.filter(publisher_is_draft=True,in_navigation = True).exclude(id__in = descendant_ids)
        quick_links_data = [
            query.id
         for query in links_excluded_data ]

        for data in value:
            glossary_data = data.get('glossary', {})
            if glossary_data:
                glossary_data['custom_menus'] = quick_links_data
            HeaderPluginModel.objects.filter(id = data['id']).update(glossary = glossary_data)
        print("Header plugin (menus) : the available menus in header section will be checked on plugin ")
