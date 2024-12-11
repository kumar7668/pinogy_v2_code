from cmsplugin_cascade.forms import CascadeModelForm
from django import forms
from cms.models import Page
from custom_design.widget import TextBoxWidget, ColorPalette, CustomCheckBox, CustomBoolean, CustomRadioSelect,CustomButton,Image, CKEditorTextboxWidget
from colorfield.widgets import ColorWidget
from pinogy_breeds.pos_api import PetTypeList
from django.utils.translation import gettext_lazy as _
from carousel_plugins.utils import get_locations_list, get_pet_status_list
from pos_api.pos_client import PWAPI
from typing import Optional
from pinogy_pet.utils import get_photos_meta, get_pet_filters
from pinogy_pet.pos_api import PetTypeList, APIPetTypeSetting, PetTypeSetting
from ..models import (
    PetDetailPluginModel, PetListPluginModel
)
PET_DETAIL=[
    ("status", _("Status")),
    ("normal_price_list", _("Price")),
    ("location", _("Location")),
    ("petname", _("Name")),
    ("breedername", _("Breed")),
    ("birthdate", _("Birthday")),
    ("sex", _("sex")),
    ("age", _("Age")),
    ("usda", _("USDA Number")),
    ("Breeder_Info", _("Breeder Info")),
    ("badges", _("Badges"))
]

class PetTypeListPluginForm(CascadeModelForm):
    """
    Store data of static info block
    """

    title = forms.CharField(
        required=False,
        widget=TextBoxWidget(
            attrs={
                "placeholder": "Enter Title",
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
        widget=TextBoxWidget(
            attrs={
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

    pet_types_list = forms.MultipleChoiceField(
        required=False,
        choices=[],
        widget=CustomCheckBox(
            attrs={
                "section_heading": "Pet Type",
                "section_sub_heading": "Select pet type  you want to be displayed",
                "section_divider": True,
            }
        ),
    )

    class Meta:
        entangled_fields = {
            "glossary": [
                "title",
                "title_color",
                "sub_title",
                "sub_title_color",
                "pet_types_list",
                # "show_tabs_pet_type",
            ]
        }
        untangled_fields = []
    
    def __init__(self, *args, **kwargs):
        super(PetTypeListPluginForm, self).__init__(*args, **kwargs)
       
        # Fetch pet types from POS
        pet_types_obj = PetTypeList()
        pet_type_unique_list = [
            (
                pet_type.id,
                pet_type.name,
            )
            for pet_type in pet_types_obj.get_pet_type_list()
        ]
        self.fields["pet_types_list"].choices = pet_type_unique_list


class PetListPluginForm(CascadeModelForm):
    """
    Store data of static info block
    """    
    
    PET_LAYOUT_CHOICES = [
        ("plugins/flow.html", _("Flow")),
        ("plugins/pet_list.html", _("Modern Contemporary")),
    ]

    IS_BUTTON=[
         ("true", _("Show")),
        ("false", _("Don't Show")),
    ]
    BUTTON_STYLE = [
        ("fill", _("Fill")),
        ("outline", _("Outline")),
    ]
    template_type = forms.ChoiceField(
        choices=PET_LAYOUT_CHOICES,
        initial="plugins/flow.html",
        required=True,
        widget=CustomRadioSelect(
            attrs={
                "section_heading": "Select Pet List Template",
                "section_divider": True,
            }
        ),
    )

    title = forms.CharField(
        required=False,
        widget=TextBoxWidget(
            attrs={
                "is_color_box_display" : True,
                "placeholder": "Enter Title",
                "label": "Title",
            }
        ),
    )

    title_color = forms.CharField(
        widget=ColorPalette(
            attrs={
                "label": "Font Color",
            },
        ),
        required=False,
    )

    sub_title = message_text = forms.CharField(required=False,widget=CKEditorTextboxWidget(
        attrs={ 
            "label" : 'Message',
            "placeholder": "Enter Message",
            }
    ))

    sub_title_color = forms.CharField(
        widget=ColorPalette(
            attrs={
                "label": "Font Color",
            },
        ),
        required=False,
    )

    pet_types_list = forms.MultipleChoiceField(
        required=False,
        choices=[],
        widget=CustomCheckBox(
            attrs={
                "section_heading": "Pet Type",
                "section_sub_heading": "Select pets you want to be displayed.",
                "section_divider": True,
            }
        ),
    )

    pet_location_filter = forms.MultipleChoiceField(
        label="Location",
        widget=CustomCheckBox(
            attrs={
                "section_heading": "Location Selection",
                "section_sub_heading": "Select a locations by which pets will be displayed.",
                "section_divider": True,
            }
        ),
        required=False,
    )

    pet_status_filter = forms.MultipleChoiceField(
        label="Status",
        widget=CustomCheckBox(
            attrs={
                "section_heading": "Pet Status",
                "section_sub_heading": "Select a statuses by which pets will be displayed.",
                "section_divider": True,
            }
        ),
        required=False,
    )

    pet_filter = forms.MultipleChoiceField(
        label="Filter",
        widget=CustomCheckBox(
            attrs={
                "section_heading": "Filter",
                "section_sub_heading": "Select criteria by which users can filter pets.",
                "section_divider": True,
            }
        ),
        required=False,
    )


    pet_detail=forms.MultipleChoiceField(
        label="PetDetail",
        choices=[],
        widget=CustomCheckBox(
            attrs={
                "section_heading": "",
                "section_sub_heading": "",
            }
        ),
        required=False,
    )
    ask_about_me = forms.ChoiceField(
        choices=IS_BUTTON,
        initial="true",
        required=False,
        widget=CustomRadioSelect(
            attrs={
                "section_heading": "",
                "section_divider": False,
            }
        ),
    )

    ask_about_me_button=forms.ChoiceField(
        choices=BUTTON_STYLE, initial="fill", required=False
    )

    more_info = forms.ChoiceField(
            choices=IS_BUTTON,
            initial="true",
            required=False,
            widget=CustomRadioSelect(
                attrs={
                    "section_heading": "",
                    "section_divider": False,
                }
            ),
        )

    more_info_button=forms.ChoiceField(
        choices=BUTTON_STYLE, initial="fill", required=False
    )

    call_now = forms.ChoiceField(
            choices=IS_BUTTON,
            initial="false",
            required=False,
            widget=CustomRadioSelect(
                attrs={
                    "section_heading": "",
                    "section_divider": False,
                }
            ),
        )
    


    call_now_button=forms.ChoiceField(
        choices=BUTTON_STYLE, initial="fill", required=False
    )
    schedule_a_play_date = forms.ChoiceField(
            choices=IS_BUTTON,
            initial="false",
            required=False,
            widget=CustomRadioSelect(
                attrs={
                    "section_heading": "",
                    "section_divider": False,
                }
            ),
        )
    schedule_a_play_button=forms.ChoiceField(
        choices=BUTTON_STYLE, initial="fill", required=False
    )


    toggle_pet_id = forms.ChoiceField(
            choices=IS_BUTTON,
            initial="false",
            required=False,
            widget=CustomRadioSelect(
                attrs={
                    "section_heading": "",
                    "section_divider": True,
                    "section_heading" : "Pet Id"
                }
            ),
        )
    button_data = forms.CharField(required=False)
    class Meta:
        model = PetListPluginModel
        entangled_fields = {
            "glossary": [
                "template_type",
                "title",
                "title_color",
                "sub_title",
                "sub_title_color",
                "pet_types_list",
                "pet_location_filter",
                "pet_status_filter",
                # "show_tabs_pet_type"
                "pet_filter",
                "pet_detail",
                "schedule_a_play_date",
                "call_now",
                "more_info",
                "ask_about_me",
                'more_info_button',
                'ask_about_me_button',
                'schedule_a_play_button',
                'call_now_button',
                "toggle_pet_id",
            ]
        }
        untangled_fields = ['button_data']
    
    def __init__(self, *args, **kwargs):
        super(PetListPluginForm, self).__init__(*args, **kwargs)
        self.client = PWAPI()

        # Fetch pet types from POS
        pet_types_obj = PetTypeList()
        pet_type_unique_list = [
            (
                pet_type.id,
                pet_type.name,
            )
            for pet_type in pet_types_obj.get_pet_type_list()
        ]
        self.fields["pet_types_list"].choices = pet_type_unique_list

        pet_setting = PetTypeSetting()
        if pet_type_unique_list:
            pt_setting = APIPetTypeSetting()
            pet_setting = pt_setting.get_pet_type_setting_obj(pet_type_unique_list[0][0])

        PET_DETAIL=[
            ("petid", _('Pet ID')),
            ("status", _("Status")),
            ("location", _("Location")),
            ("petname", _("Name")),
            ("breedername", _("Breed")),
            ("birthdate", _("Birthday")),
            ("sex", _("sex")),
            ("age", _("Age")),
            ("usda", _("USDA Number")),
            ("Breeder_Info", _("Breeder Info")),
            ("badges", _("Badges"))

        ]
        
        for atr in PET_DETAIL:
            if hasattr(pet_setting, atr[0]):
             if not getattr(pet_setting, atr[0]).visible:
                PET_DETAIL.pop(PET_DETAIL.index(atr))
            else:
                PET_DETAIL.pop(PET_DETAIL.index(atr))

        self.fields["pet_detail"].choices=PET_DETAIL

        # Fetch pet locations from pos
        locations_list = [
            (location["id"], location["name"])
            for location in get_locations_list(client=self.client)
        ]
        self.fields["pet_location_filter"].choices = locations_list
        self.fields["pet_detail"].choices = PET_DETAIL

        # Fetch pet statues from POS
        pet_status_list = [
            (pet_status["id"], pet_status["name"])
            for pet_status in get_pet_status_list(client=self.client)
            if pet_status["available_publicly"] is True
        ]


        pet_status_list_=self.get_pet_filters(client=self.client,pet_type_name=None)
        pet_filter_list =[
            (pet_status["param"], pet_status["name"])
            for pet_status in pet_status_list_["filters"]
            if pet_status["enabled"] is True
        ] 

        self.fields["pet_status_filter"].choices = pet_status_list
        self.fields["pet_filter"].choices =pet_filter_list#[get_pet_filters(client=self.client,pet_type_name=None)]
        
    def get_pet_filters(self, client: Optional[PWAPI] = None, pet_type_name: Optional[str] = None):
    
        

        api_pet_list_filters = get_pet_filters(client=client, pet_type_name=pet_type_name)

        pet_list_filters = {'filter_values': {}, 'filters':[]}
        for k,v in api_pet_list_filters.get('filter_values').items():
            if v and isinstance(v, dict) and len(v) > 1:
                pet_list_filters['filter_values']['qp_'+k] = dict(sorted(v.items()))

        for filter in api_pet_list_filters.get('filters'):
            if pet_list_filters.get('filter_values').get(filter.get('param')) and filter.get('enabled'):
                pet_list_filters.get('filters').append(filter)
            elif pet_list_filters.get('filter_values').get(filter.get('param')):
                pet_list_filters.get('filter_values').pop(filter.get('param'))

        return pet_list_filters

class PetDetailPluginForm(CascadeModelForm):
    """
    Store data of static info block
    """

    PET_LAYOUT_CHOICES = [
        ("true", _("Show")),
        ("false", _("Don’t show")),
    ]

    CONSUMER_VERIFICATION_LAYOUT_CHOICES = [
        ("true", _("Show")),
        ("false", _("Don’t show")),
    ]

    LINK_CHOICES = [
        ("Internal link", _("Internal link"),),
        ("External link", _("External link"),),
    ]


    BUTTON_TYPE=[
        ("schedule_a_playdate", _("Schedule a Playdate")),
        ("take_me_home", _("Take Me Home")),
        ("ask_about_me", _("Ask About Me")),
        ("call_now", _("Call Now")),
        ("make_an_offer", _("Make an Offer")),
        ("other", _("Other")),
    ]

    BUTTON_TARGET_CHOICES = [
        ("_self", _("Same Window"),),
        ("_blank", _("New Window"),),
    ]

    BUTTON_STYLE = [
        ("fill", _("Fill")),
        ("outline", _("Outline")),
    ]

    BUTTON_CHOICES=[
        ("", "-----"),
        ("schedule_a_playdate", _("Schedule a Playdate")),
        ("ask_about_me", _("About Breed")),
        ("call_now", _("Call Now")),
        ("link", _("Link")),
    ]

    BUTTON_SETTINGS=[
        ("top", _("Place this button at the top of the page.")),
        ("width", _("Show this button in full width.")),
    ]

    pet_detail=forms.MultipleChoiceField(
        label="PetDetail",
        choices=[],
        widget=CustomCheckBox(
            attrs={
                "section_heading": "",
                "section_sub_heading": "",
                "section_divider": True,
            }
        ),
        required=False,
    )


    consumer_verification = forms.ChoiceField(
        choices=CONSUMER_VERIFICATION_LAYOUT_CHOICES,
        initial="false",
        required=True,
        widget=CustomRadioSelect(
            attrs={
                "section_heading": "Consumer Verification",
                "horizontal_layout": True,
            }
        ),
    )

    promotion_banner = forms.ChoiceField(
        choices=PET_LAYOUT_CHOICES,
        initial="false",
        required=True,
        widget=CustomRadioSelect(
            attrs={
                "section_heading": "Promotion Banner",
                "horizontal_layout": True,
            }
        ),
    )

    promob_image = forms.ImageField(
        label="Upload Image",
        help_text="Drop files or click to upload",
        required=False
    )

    alt_name_promob_image = forms.CharField(required=False,widget=TextBoxWidget(
        attrs= { 
            "is_color_box_display": False,
            "placeholder": "Enter ALT text",
            }
    ))

    button_type = forms.ChoiceField(
        choices=BUTTON_TYPE,
        required=False,
        widget=CustomRadioSelect(
            attrs={
                "section_heading": "Button Type",
                "section_divider": False,
            }
        ),
    )

    btn_type_link_choice = forms.ChoiceField(
        choices= LINK_CHOICES,
        widget= CustomRadioSelect(
            attrs={
                "horizontal_layout" : True,
            }
        ),
        required = False
    )

    btn_type_internal_link = forms.ModelChoiceField(
        blank=True,
        required=False,
        queryset=Page.objects.filter(publisher_is_draft=False),
    )

    btn_type_external_link = forms.URLField(required=False)

    more_about_breed =  forms.BooleanField(initial=False,required=False)

    # Buttons section

    button_data = forms.CharField(required=False)

    button_internallink_1 = forms.ModelChoiceField(
        blank=True,
        required=False,
        queryset=Page.objects.filter(publisher_is_draft=False),
    )

    link_choice_field_btn1 = forms.ChoiceField(
        choices= LINK_CHOICES,
        widget= CustomRadioSelect(
            attrs={
                "horizontal_layout" : True,
            }
        ),
        required = False
    )

    first_button_text = forms.CharField(required=False)

    first_button_link = forms.URLField(required=False)

    first_button_style = forms.ChoiceField(
        # widget=CustomButtonStyle(
        # ),
        choices=BUTTON_STYLE, initial="fill", required=False
    )

    first_button_fill_color = forms.CharField(
        widget=ColorWidget({"format": "hexa"}), initial="#ffffffff", required=False
    )

    first_button_font_color = forms.CharField(
        widget=ColorWidget({"format": "hexa"}), initial="#000000ff", required=False
    )

    first_button_outline_color = forms.CharField(
        widget=ColorWidget({"format": "hexa"}), initial="#000000ff", required=False
    )

    first_button_color_pattern = forms.CharField(
        # widget=CustomButtonColor(
        # ),
        required=False)

    button_selector_1 = forms.ChoiceField(
        choices = BUTTON_CHOICES,
        required = False,
        initial="",
        widget=forms.Select(attrs={
            'id': 'id_button_selector-1',
        })
    )

    button_settings_1 = forms.ChoiceField(
        choices = BUTTON_SETTINGS,
        required = False,
        widget=CustomCheckBox(
            attrs={
                'id': 'id_button_settings',
            }
        ),
    )

    #Ask About Pet form

    message = forms.CharField(
        required=False,
        widget=TextBoxWidget(
            attrs={
                "placeholder": "Enter message",
                "label": "Message",
            }
        ),
    )

    petform_button_style = forms.CharField(
        initial="fill", required=False
    )


    class Meta:
        model = PetDetailPluginModel
        entangled_fields = {
            "glossary": [
                "pet_detail",
                "promotion_banner",
                "alt_name_promob_image",
                "button_type",
                "more_about_breed",
                "btn_type_link_choice",
                "btn_type_internal_link",
                "btn_type_external_link",
                "button_internallink_1",
                "link_choice_field_btn1",
                "first_button_text",
                "first_button_link",
                "first_button_style",
                "first_button_fill_color",
                "first_button_font_color",
                "first_button_outline_color",
                "first_button_color_pattern",
                "button_selector_1",
                "button_settings_1",
                "message",
                "petform_button_style",
                "consumer_verification"
            ]
        }
        untangled_fields = ["promob_image","button_data"]
    
    def __init__(self, *args, **kwargs):
        super(PetDetailPluginForm, self).__init__(*args, **kwargs)

        self.client = PWAPI()

        # Fetch pet types from POS
        pet_types_obj = PetTypeList()
        pet_type_unique_list = [
            (
                pet_type.id,
                pet_type.name,
            )
            for pet_type in pet_types_obj.get_pet_type_list()
        ]
        pet_setting = PetTypeSetting()
        if pet_type_unique_list:
            pt_setting = APIPetTypeSetting()
            pet_setting = pt_setting.get_pet_type_setting_obj(pet_type_unique_list[0][0])

        PET_DETAIL=[
            ("status", _("Status")),
            ("normal_price_list", _("Price")),
            ("location", _("Location")),
            ("petname", _("Name")),
            ("breedername", _("Breed")),
            ("birthdate", _("Birthday")),
            ("sex", _("sex")),
            ("age", _("Age")),
            ("usda", _("USDA Number")),
            ("Breeder_Info", _("Breeder Info")),
            ("badges", _("Badges"))

        ]
        for atr in PET_DETAIL:
            if hasattr(pet_setting, atr[0]):
             if not getattr(pet_setting, atr[0]).visible_detail_only:
                PET_DETAIL.pop(PET_DETAIL.index(atr))
            else:
                PET_DETAIL.pop(PET_DETAIL.index(atr))
        self.fields["pet_detail"].choices=PET_DETAIL

class PetPurchaseForm(CascadeModelForm):
    """
    Store data of PetPurchaseForm
    """

    DEFAULT_DEPOSIT_AMOUNT = 300.00
    MIN_DEPOSIT_AMOUNT = 100.00
    DEFAULT_DEPOSIT_MESSAGE = "{deposit_amount} is a deposit and will be collected on the next screen and will hold the pet. The deposit amount is non-refundable."
    DEFAULT_SECTION_NAME = "Adopt Me"

    ONLY_DEPOSIT_PAYMENT = "Only Deposit Payment"
    ONLY_FULL_PAYMENT = "Only Full Payment"
    BOTH_METHODS = "Both Methods"

    PAYMENT_METHOD_CHOICES = [
        (ONLY_DEPOSIT_PAYMENT, ONLY_DEPOSIT_PAYMENT),
        (ONLY_FULL_PAYMENT, ONLY_FULL_PAYMENT),
        (BOTH_METHODS, BOTH_METHODS),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        initial=BOTH_METHODS,
        required=True,
        widget=CustomRadioSelect(
            attrs={
                "section_heading": "Select Payment Methods",
                "section_divider": True,
            }
        ),
    )

    deposit_amount = forms.FloatField(
        required=True,
        initial=DEFAULT_DEPOSIT_AMOUNT,
        min_value=MIN_DEPOSIT_AMOUNT,
        widget=TextBoxWidget(
            attrs={
                "input_type": "number",
                "label": "Deposit Amount",
                "section_divider": True,
            }
        ),
    )

    deposit_message = forms.CharField(
        required=True,
        initial=DEFAULT_DEPOSIT_MESSAGE,
        help_text="Use {deposit_amount} for dynamic Deposit amount value.",
        widget=TextBoxWidget(
            attrs={
                "input_type": "text",
                "label": "Deposit Message",
            }
        ),
    )

    section_name = forms.CharField(
        required=True,
        initial=DEFAULT_SECTION_NAME,
        help_text="Please enter the section name that will be displayed on the button and as the title of the popup.",
        widget=TextBoxWidget(
            attrs={
                "input_type": "text",
                "label": "Section Name",
            }
        ),
    )

    class Meta:
        entangled_fields = {
            "glossary": [
                "payment_method",
                "deposit_amount",
                "deposit_message",
                "section_name",
            ]
        }
        untangled_fields = []
    
    def __init__(self, *args, **kwargs):
        super(PetPurchaseForm, self).__init__(*args, **kwargs)