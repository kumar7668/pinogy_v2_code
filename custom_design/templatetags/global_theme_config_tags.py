# -*- coding: utf-8 -*-
from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag
from django import template

from custom_design.models import ThemeConfiguration

register = template.Library()


class GlobalThemeConfigTag(AsTag):
    """
    Retrieves an item from the Site Configuration, if found.
    """

    name = "global_theme_object"
    options = Options(
        Argument("setting", required=False, resolve=True),
        "as",
        Argument("varname", required=False, resolve=False),
    )

    def get_value(self, context, setting):
        try:
            return ThemeConfiguration.objects.get()
        except Exception as e:
            print("Except : ", str(e))
            return None


register.tag(GlobalThemeConfigTag)
