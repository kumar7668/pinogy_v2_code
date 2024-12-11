from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import TemplateConfig, ThemeConfiguration, ThemeImages


class ThemeConfigAdmin(SingletonModelAdmin):
    pass


class TemplateConfigAdmin(SingletonModelAdmin):
    pass


admin.site.register(TemplateConfig, TemplateConfigAdmin)
admin.site.register(ThemeConfiguration, ThemeConfigAdmin)
admin.site.register(ThemeImages)
