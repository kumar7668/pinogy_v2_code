from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

class Command(BaseCommand):
    help = 'Reset content types and permissions by deleting existing data and loading default data.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Running the migrate command...'))
        call_command('migrate')

        self.stdout.write(self.style.SUCCESS('Deleting existing content types and permissions...'))
        ContentType.objects.all().delete()
        Permission.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Loading default data...'))
        call_command('loaddata', 'initialdata.json')

        self.stdout.write(self.style.SUCCESS('Loading complete!'))
