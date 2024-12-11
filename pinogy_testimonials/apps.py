from django.apps import AppConfig


class PinogyTestimonialsConfig(AppConfig):
    name = 'pinogy_testimonials'

    def ready(self):
        import pinogy_testimonials.signals
