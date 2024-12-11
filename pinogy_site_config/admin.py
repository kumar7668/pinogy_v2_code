from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import SiteConfig

class SiteConfigAdmin(SingletonModelAdmin):
    pass


admin.site.register(SiteConfig, SiteConfigAdmin)