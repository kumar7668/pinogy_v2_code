from django.dispatch import receiver
from cms.models import Page
from cms.signals import post_publish, post_unpublish
from django.db.models.signals import post_delete

from .utils import send_page_data_to_api

@receiver([post_publish, post_unpublish, post_delete], sender=Page)
def handle_publish_unpublish(sender, instance, **kwargs):
    """
    Signal handler for post_publish, post_unpublish and post_delete signals.
    """
    send_page_data_to_api()
