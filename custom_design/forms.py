from django import forms
from django.utils.translation import ugettext_lazy as _

from custom_design.models import ThemeConfiguration


class ThemeConfigurationForm(forms.ModelForm):
    FONT_CHOICES = [
        ("'Open Sans', Arial, sans-serif", _("Open Sans")),
        ("'Poppins', sans-serif", _("Poppins")),
        ("'Spectral', serif", _("Spectral")),
        ("'ClashDisplay-Variable', sans-serif", _("ClashDisplay-Variable")),
        ("'Inter', sans-serif", _("Inter")), 
        ("'Philosopher', sans-serif", _("Philosopher")),
        ("'Nunito', sans-serif", _("Nunito")),
        ("'Geometric Slabserif 703 Bold', sans-serif", _("Geometric Slabserif 703 Bold")),
        ("'Baloo 2', sans-serif", _("Baloo 2")),
        ("'Fredoka', cursive", _("Fredoka")),
        ("'Mermaid', sans-serif", _("Mermaid")),
        ("'Comfortaa', cursive", _("Comfortaa")),
    ]
    default_font = '"Open Sans", Arial, sans-serif'
    
    background = forms.ImageField(required=False)
    logo = forms.ImageField(required=False)
    favicon = forms.ImageField(required=False)
    heading_font = forms.ChoiceField(
        initial=default_font, choices=FONT_CHOICES
    )
    general_font = forms.ChoiceField(
        initial=default_font, choices=FONT_CHOICES
    )

    button_font = forms.ChoiceField(
        initial=default_font, choices=FONT_CHOICES
    )

    class Meta:
        model = ThemeConfiguration
        exclude = ["selected_logo", "selected_favicon", "file_version"]
