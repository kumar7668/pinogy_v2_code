import logging

from django import template
from django.core.cache import cache
from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag
from pos_api.cached_response import get_pos_integration_data
from pinogy_site_config.models import SiteConfig

logger = logging.getLogger('django.request')
register = template.Library()

class SiteConfigTag(AsTag):
    """
    Retrieves the Site Configuration object, if found.
    """
    name = 'site_config_tag'
    options = Options(
        'as',
        Argument('varname', required=False, resolve=False)
    )

    def get_value(self, context):
        return {
            "site_config": SiteConfig.get_cached_site_config(),
            "pos_config": get_pos_integration_data(),
        }

register.tag(SiteConfigTag)