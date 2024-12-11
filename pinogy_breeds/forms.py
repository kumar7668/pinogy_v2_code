from cmsplugin_cascade.forms import CascadeModelForm
from django import forms
from django.utils.translation import ugettext as _
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from custom_design.widget import TextBoxWidget, ColorPalette, CustomCheckBox, CustomRadioSelect
from pinogy_breeds.pos_api import PetTypeList
from .models import BreedDetailPluginModel



class BreedTypeListPluginForm(CascadeModelForm):
    """
    Breed Type List Plugin Form
    """

    PET_LAYOUT_CHOICES = [
        ("pinogy_breeds/plugins/breed_type_list.html", _("Standard Breed Template")),
        ("pinogy_breeds/plugins/breed_list_without_image.html", _("Breed List Without Images")),
    ]
    
    template_type = forms.ChoiceField(
        choices=PET_LAYOUT_CHOICES,
        initial="pinogy_breeds/plugins/breed_type_list.html",
        required=True,
        widget=CustomRadioSelect(
            attrs={
                "section_heading": "Select Breed List Template",
                "section_divider": True,
            }
        ),
    )

    title = forms.CharField(
        required=False,
        widget=TextBoxWidget(
            attrs={
                "placeholder": "Enter Title",
                "is_color_box_display": True,
                "label": "Title",
                "section_heading": "Text"
            }
        ),
    )

    title_color = forms.CharField(
        # widget=ColorWidget({"format": "hexa"}), initial="#ffffffff", required=False,
        widget=ColorPalette(
            attrs={
                "label": "Font Color",
            },
        ),
        required=False,
    )

    sub_title = forms.CharField(
        required=False,
        widget=TextBoxWidget(attrs={
            "is_color_box_display": True,
            "placeholder": "Enter Sub Title",
            "label": "Sub Title",
        }, )
    )

    sub_title_color = forms.CharField(
        # widget=ColorWidget({"format": "hexa"}), initial="#ffffffff", required=False,
        widget=ColorPalette(
            attrs={
                "label": "Font Color",
                "section_divider": True,
            },
        ),
    )

    breeds_pet_type = forms.MultipleChoiceField(
        required=False,
        choices=[],
        widget=CustomCheckBox(
            attrs={
                "section_heading": "Breeds by Pet Type",
                "section_heading_desc": "Select pet type breeds you want to be displayed",
                "section_divider": True,
            }
        ),
    )

    show_tabs_pet_type = forms.ChoiceField(
        choices=[(True, "Show"), (False, "Don't Show")],
        widget=CustomRadioSelect(
            attrs={
                "section_heading": "Breed Tabs by Pet Type",
                "section_divider": True,
            }
        ),
    )

    class Meta:
        entangled_fields = {
            "glossary": [
                "template_type",
                "title",
                "title_color",
                "sub_title",
                "sub_title_color",
                "breeds_pet_type",
                "show_tabs_pet_type",
            ]
        }
        untangled_fields = []
    
    def __init__(self, *args, **kwargs):
        super(BreedTypeListPluginForm, self).__init__(*args, **kwargs)
       
        # Fetch pet types from POS
        pet_types_obj = PetTypeList()
        pet_type_unique_list = [
            (
                pet_type.id,
                pet_type.selected_plural,
            )
            for pet_type in pet_types_obj.get_pet_type_list()
        ]
        self.fields["breeds_pet_type"].choices = pet_type_unique_list
        
class BreedDetailPluginForm(CascadeModelForm):
    """
     Breed Detail plugin Form
    """
    TRAITS_LAYOUT_CHOICES = [
        ("LAYOUT1", _("Simple Line")),
        ("LAYOUT2", _("Circle")),
        ("LAYOUT3", _("Bar")),
    ]

    message = forms.CharField(
        required=False,
        widget=TextBoxWidget(
            attrs={
                "placeholder": "Enter message",
                "label": "Message",
            }
        ),
    )

    breedform_button_style = forms.CharField(
        initial="fill", required=False
    )

    show_breed_traits = forms.ChoiceField(
        choices=[(True, "Show"), (False, "Don't Show")],
        initial="True",
        widget=CustomRadioSelect(
            attrs={
                "section_heading": "Breed Traits",
                "horizontal_layout" : True,
            }
        ),
    )

    traits_layouts = forms.ChoiceField(
        choices=TRAITS_LAYOUT_CHOICES,
        initial="LAYOUT1",
        widget=CustomRadioSelect(),
    )

    show_breed_notes = forms.ChoiceField(
        required=False,
        initial="True",
        choices=[(True, "Show"), (False, "Don't Show")],
        widget=CustomRadioSelect(
            attrs={
                "section_heading": "Breed Notes",
                 "horizontal_layout" : True,
            }
        ),
    )
    class Meta:
        model = BreedDetailPluginModel
        entangled_fields = {
            "glossary": [
                "message",
                "breedform_button_style",
                "show_breed_traits",
                "traits_layouts",
                "show_breed_notes",
            ]
        }
        untangled_fields = []