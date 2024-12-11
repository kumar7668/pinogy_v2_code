from django.core.management.base import BaseCommand
from custom_design.models import ThemeConfiguration

class Command(BaseCommand):
    help = 'Save theme config model'

    def handle(self, *args, **options):
        try:
            theme_config_obj = ThemeConfiguration.objects.get()
            theme_config_obj.save()
        except Exception as e:
            print("Except : ", str(e))