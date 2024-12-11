from cms.models.pluginmodel import CMSPlugin
from django.db import models

class BaseFieldPluginModel(CMSPlugin):
    """
    Base class for storing data of Field Plugins
    """

    label = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, help_text="Used to set the field name")
    placeholder_text = models.CharField(
        null=True, blank=True,
        max_length=255,
        verbose_name="Placeholder Text",
        help_text='Default text in a form. Disappears when the user starts typing. Example: "email@example.com"'
    )
    is_required = models.BooleanField(verbose_name="Field is required", default=False)

    class Meta:
        abstract = True

class FormPluginModel(CMSPlugin):
    """
    Store data of Form Plugins
    """

    form_name = models.CharField(max_length=255, verbose_name="Form Name")


class TextFieldPluginModel(BaseFieldPluginModel):
    """
    Store data of Text Field Plugins
    """

    pass

class EmailFieldPluginModel(BaseFieldPluginModel):
    """
    Store data of Email Field Plugins
    """

    pass

class NumberFieldPluginModel(BaseFieldPluginModel):
    """
    Store data of Number Field Plugins
    """

    pass

class PhoneNumberFieldPluginModel(BaseFieldPluginModel):
     """
     Store data of Phone Number Field Plugins
     """

     pass

class TextAreaFieldPluginModel(BaseFieldPluginModel):
    """
    Store data of Text Area Field Plugins
    """

    pass

class CheckBoxFieldPluginModel(BaseFieldPluginModel):
    """
    Store data of Text Area Field Plugins
    """

    # Override the placeholder_text field for CheckBoxFieldPluginModel
    placeholder_text = None

    # Option to specify whether the checkbox should be checked by default
    default = models.BooleanField(
        verbose_name="Default",
        default=False,
        help_text="Check this box to have the checkbox pre-checked by default"
    )

    pass

class LocationFieldPluginModel(BaseFieldPluginModel):
    """
    Store data of Text Area Field Plugins
    """

    # Override the placeholder_text field for CheckBoxFieldPluginModel
    placeholder_text = None

    pass

class MarketingFieldPluginModel(BaseFieldPluginModel):
    """
    Store data of Text Area Field Plugins
    """

    # Override the placeholder_text , name and label field for MarketingFieldPluginModel
    placeholder_text = None
    label = None
    name = None

    default_location = models.IntegerField(
        verbose_name="Selected Location",
        help_text="The marketing location selected from the list",
        null=True,
        blank=True
    )

class DateTimeFieldPluginModel(BaseFieldPluginModel):
    """
    Store data of Text Field Plugins
    """

    # Override the placeholder_text , name and label field for MarketingFieldPluginModel
    placeholder_text = None
    
    pass

class DropdownPluginModel(BaseFieldPluginModel):
    """
    Store data of Dropdown Field Plugins
    """
    values = models.JSONField(default=list, help_text="Enter multiple values for the dropdown")

    def __str__(self):
        return self.name
