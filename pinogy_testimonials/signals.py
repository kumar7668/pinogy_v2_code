from .models import Testimonial
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save


@receiver([post_delete, post_save], sender=Testimonial)
def clear_testimonials_when_delete(sender, instance, **kwargs):
    cache.delete('pinogy_testimonials:testimonial_carousel:testimonial_list')
