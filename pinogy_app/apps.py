from django.apps import AppConfig

class PinogyAppConfig(AppConfig):
    name = "pinogy_app"

    def ready(self):
        import pinogy_app.signals
