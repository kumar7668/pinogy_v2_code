from solo.models import SingletonModel
from django.core.cache import cache
from django.db import models

SITE_CONFIG_CACHE_KEY = "site_config_cache"
SITE_CONFIG_CACHE_TIMEOUT = 6 * 30 * 24 * 60 * 60  # Cache for 6 months in seconds 

class SiteConfig(SingletonModel):

    header_block = models.TextField(default='', blank=True, help_text="This will be added to header block.")

    body_top_block = models.TextField(default='', blank=True, help_text="This will be added to top of the body block.")

    body_bottom_block = models.TextField(default='', blank=True,  help_text="This will be added to bottom of the body block.")

    class Meta:
        verbose_name = 'site configuration'
        verbose_name_plural = 'site configuration'

    def __str__(self):
        return 'Site Config'

    @staticmethod
    def get_cached_site_config():
        """ 
            If site config does not exist in cache or is not a dictionary, attempt to fetch it from the database.
            If data is not there then create blank entry
        """
        config = cache.get(SITE_CONFIG_CACHE_KEY)

        if config is None:
            config, _ = SiteConfig.objects.get_or_create()
            cache.set(SITE_CONFIG_CACHE_KEY, config, SITE_CONFIG_CACHE_TIMEOUT)

        return config

    def save(self, *args, **kwargs):
        cache.set(SITE_CONFIG_CACHE_KEY, self, SITE_CONFIG_CACHE_TIMEOUT)
        super().save(*args, **kwargs)
