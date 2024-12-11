from django.core import management, cache


class Command(management.base.BaseCommand):
    help = "Complex command for running static collection, migration and cache clearing."

    def handle(self, *args, **options):
        management.call_command('migrate')
        management.call_command('save_theme_config')

        # management.call_command('collectstatic', interactive=False)
        # cache.cache.clear()