from cms.models import Page
from cmsplugin_cascade.forms import CascadeModelForm
from colorfield.widgets import ColorWidget
from django import forms
from django.utils.translation import gettext_lazy as _
from cmsplugin_cascade.models import InlineCascadeElement
from django.contrib.admin import StackedInline, TabularInline
from cmsplugin_cascade.fields import CascadeImageField
from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from django.forms.widgets import FileInput

from pos_api.pos_client import PWAPI
from custom_design.models import ThemeImages, ThemeConfiguration
from custom_design.widget import TextBoxWidget, ColorPalette, LinkWidget, CustomCheckBox, CustomRadioSelect, CKEditorTextboxWidget
from .utils import get_stores_data
from django.core.validators import FileExtensionValidator
from .models import (
    BannerPluginModel,
    FooterPluginModel,
    HeaderPluginModel,
    InfoBlockFirstPluginModel,
    InfoBlockSecondPluginModel,
    SliderPluginModel,
    GalleryPluginModel,
    SubscribePluginModel,
    UnSubscribePluginModel,
)
from pinogy_shop.pos_api.customer import EntityClient
from carousel_plugins.utils import get_locations_list

ISBUTTON_CHOICES = [
    (False, _("False")),
    (True, _("True"))
        ]

class DateRangeField(forms.CharField):
    def clean(self, value):
        # Clean the input value
        cleaned_value = super(DateRangeField,self).clean(value)
        return cleaned_value

class BannerPluginForm(CascadeModelForm):

    LAYOUT_CHOICES = [
        ("TEXT 1 BUTTON LEFT", _("Text and 1 Button on left")),
        ("TEXT 1 BUTTON RIGHT", _("Text and 1 Button on right")),
        ("TEXT 2 BUTTONS LEFT", _("Text and 2 Button on left")),
        ("TEXT 2 BUTTONS RIGHT", _("Text and 2 Button on right")),
        ("TEXT 1 BUTTON CENTER", _("Text and 1 Button in center ")),
        ("TEXT 2 BUTTONS CENTER", _("Text and 2 Buttons in center")),
        ("IMAGE ONLY", _("Image Only")),
    ]
    MOBILE_LAYOUT_CHOICES = [
        ("mobile_layout_1", _("mobile_layout_1")),
        ("mobile_layout_2", _("mobile_layout_2")),
        ("mobile_layout_3", _("mobile_layout_3")),
        ("mobile_layout_4", _("mobile_layout_4")),
        ("mobile_layout_5", _("mobile_layout_5")),
    ]

    BUTTON_STYLE = [
        ("fill", _("Fill")),
        ("outline", _("Outline")),
    ]

    
    PARALLAX_CHOICES = [
        (True, 'Enable'),
        (False, 'Disable'),
    ]

    LINK_CHOICES = [
        ("Internal link", _("Internal link"),),
        ("External link", _("External link"),),
        ("Phone link", _("Phone link"),),
    ]

    BUTTON_TARGET_CHOICES = [
        ("_self", _("Same Window"),),
        ("_blank", _("New Window"),),
    ]

    layout = forms.ChoiceField(
        choices=LAYOUT_CHOICES,
        label="Banner's Layout",
        initial="TEXT 1 BUTTON LEFT",
        help_text="Specify the layout of banner section.",
        widget=forms.RadioSelect(),
    )

    mobile_layout = forms.ChoiceField(
        choices=MOBILE_LAYOUT_CHOICES,
        label="Banner's mobile Layout",
        initial="mobile_layout_1",
        help_text="Specify the layout of banner section for mobile view.",
        widget=forms.RadioSelect(),
    )

    image = forms.ImageField(
        label="Upload Image",
        help_text="Upload your .JPG, .PNG, .SVG, .WEBP or .GIF files here.",
    )
    
    mobimage = forms.ImageField(
        label="Upload Image",
        help_text="Upload your .JPG, .PNG, .SVG, .WEBP or .GIF files here.",
        required=False
    )

    parallax = forms.ChoiceField(
        choices=PARALLAX_CHOICES,
        label="Parallax Effect",
        initial="False",
        widget=CustomRadioSelect(
            attrs={
                "section_heading": "Parallax Effect",
            }
        ),
        required=False
    )

    x_perc = forms.CharField(required=False)
    y_perc = forms.CharField(required=False)

    POSITION_CHOICES = [
        ("TOP", _("TOP")),
        ("CENTER", _("CENTER")),
        ("BOTTOM", _("BOTTOM")),
    ]

    content_pos = forms.ChoiceField(
        choices=POSITION_CHOICES,
        label="Banner's Content Position",
        initial="BOTTOM",
        help_text="Specify the position of banner content.",
        widget=forms.RadioSelect(),
        required=False
    )

    BANNER_TYPE_CHOICES = [
        ("PRIMARY", _("PRIMARY")),
        ("SECONDARY", _("SECONDARY")),
    ]

    banner_type = forms.ChoiceField(
        choices=BANNER_TYPE_CHOICES,
        label="Banner Type",
        initial="SECONDARY",
        help_text="Specify the type of banner.",
        widget=forms.RadioSelect(),
        required=False
    )

    banner_height = forms.IntegerField(
        widget=TextBoxWidget(
            attrs={
                "input_type": "number",
                "placeholder": "Enter Height",
            }
        ),
        required=False
    )

    title_text = forms.CharField(
        widget=TextBoxWidget(
            attrs={
                "is_color_box_display": True,
                "label": "Title",
            },
        ),
        required=False)

    title_text_color = forms.CharField(
       widget=ColorPalette(
            attrs={
                "label": "Title Color",
            },
        ), 
        required=False
    )

    sub_title_text = forms.CharField(
        widget=TextBoxWidget(
            attrs={
                "is_color_box_display": True,
                "label": "Subtitle",
            },
        ),
        required=False)

    sub_title_text_color = forms.CharField(
        widget=ColorPalette(
            attrs={
                "label": "Subtitle Color",
            },
        ), 
        required=False
    )

    image_clickable = forms.ChoiceField(
        choices=PARALLAX_CHOICES,
        label="Image Click",
        initial="False",
        widget=CustomRadioSelect(
            attrs={
                "horizontal_layout": "True"
            }
        ),
        required=False
    )

    img_link_choice_field = forms.ChoiceField(
        choices= LINK_CHOICES,
        initial= 'Internal link',
        widget= CustomRadioSelect(
            attrs={
                "horizontal_layout" : True,
            }
        ),
        required = False
    )

    img_first_button_link = forms.URLField(required=False)

    img_internallink = forms.ModelChoiceField(
        blank=True,
        required=False,
        queryset=Page.objects.filter(publisher_is_draft=False),
    )

    img_phone_link = forms.CharField(required=False)

    img_button_target = forms.ChoiceField(
        choices=BUTTON_TARGET_CHOICES,
        label="BUTTON_TARGET",
        initial="_self",
        help_text="Specify the target of button.",
        widget=forms.Select(),
        required=False,
    )

    first_button_text = forms.CharField(required=False)

    first_button_link = forms.URLField(required=False)

    button_internallink_1 = forms.ModelChoiceField(
        blank=True,
        required=False,
        queryset=Page.objects.filter(publisher_is_draft=False),
    )
    first_button_internallink = forms.ModelChoiceField(
        blank=True,
        required=False,
        queryset=Page.objects.filter(publisher_is_draft=False),
    )

    first_button_target = forms.ChoiceField(
        choices=BUTTON_TARGET_CHOICES,
        label="BUTTON_TARGET",
        initial="_self",
        help_text="Specify the target of button.",
        widget=forms.Select(),
        required=False,
    )
    second_button_target = forms.ChoiceField(
        choices=BUTTON_TARGET_CHOICES,
        label="BUTTON_TARGET",
        initial="_self",
        help_text="Specify the target of button.",
        widget=forms.Select(),
        required=False,
    )
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

    second_button_text = forms.CharField(required=False)

    second_button_link = forms.URLField(required=False)

    second_button_internallink = forms.ModelChoiceField(
        blank=True,
        required=False,
        queryset=Page.objects.filter(publisher_is_draft=False),
    )

    second_button_style = forms.ChoiceField(
        choices=BUTTON_STYLE, initial="fill", required=False
    )

    second_button_fill_color = forms.CharField(
        widget=ColorWidget({"format": "hexa"}), initial="#ffffffff", required=False
    )

    second_button_font_color = forms.CharField(
        widget=ColorWidget({"format": "hexa"}), initial="#000000ff", required=False
    )

    second_button_outline_color = forms.CharField(
        widget=ColorWidget({"format": "hexa"}), initial="#000000ff", required=False
    )

    second_button_color_pattern = forms.CharField(required=False)

    # for image alt name 
    alt_name = forms.CharField(
        widget=TextBoxWidget(
            attrs={
                "input_type": "text",
                "placeholder": "Enter ALT text",
            }
        ),
        required=False
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
    link_choice_field_btn2 = forms.ChoiceField(
        choices= LINK_CHOICES,
        widget= CustomRadioSelect(
            attrs={
                "horizontal_layout" : True,
            }
        ),
        required = False
    )

    first_button_phone_link = forms.CharField(required=False)
    second_button_phone_link = forms.CharField(required=False)

    messages = forms.CharField(widget=CKEditorTextboxWidget(
        attrs={ 
            "placeholder": "Write message here",
            }
    ),required=False)

    message_font_color = forms.CharField(
        widget=ColorPalette(
            attrs={
                "label": "Font Color",
            },
        ), 
        required=False
    )

    button_data = forms.CharField()

    BTN_DIRECTION = [
        ('horizontal',_('Horizontal'),),
        ('vertical',_('Vertical'),),
    ]
    button_direction = forms.ChoiceField(
        choices= BTN_DIRECTION,
        widget= CustomRadioSelect(
            attrs={
                "horizontal_layout" : True,
            }
        ),
        required = False
    )
    class Meta:
        model = BannerPluginModel
        entangled_fields = {
            "glossary": [
                "layout",
                "mobile_layout",
                "banner_height",
                "title_text",
                "title_text_color",
                "sub_title_text",
                "sub_title_text_color",
                "first_button_text",
                "first_button_link",
                "first_button_internallink",
                "first_button_style",
                "first_button_fill_color",
                "first_button_font_color",
                "first_button_outline_color",
                "first_button_color_pattern",
                "second_button_color_pattern",
                "second_button_text",
                "second_button_link",
                "second_button_internallink",
                "second_button_style",
                "second_button_fill_color",
                "second_button_font_color",
                "second_button_outline_color",
                "content_pos",
                "banner_type",
                "first_button_target",
                "second_button_target",
                "x_perc",
                "y_perc",
                "parallax",
                "alt_name",  
                "link_choice_field_btn1",
                "link_choice_field_btn2",
                "first_button_phone_link",
                "second_button_phone_link",
                'messages',
                'message_font_color',
                'button_internallink_1',
                'button_direction',
                'image_clickable',
                'img_link_choice_field',
                'img_first_button_link',
                'img_phone_link',
                'img_button_target',
                'img_internallink'
            ]
        }
        untangled_fields = ["image","mobimage",'button_data']

class PopupPluginForm(CascadeModelForm):

    btn_text = forms.CharField(
        widget=TextBoxWidget(
            attrs={
                "label": "Button Text",
            },
        ),
        required=False)
    popuptitle = forms.CharField(
        widget=TextBoxWidget(
            attrs={
                "is_color_box_display": True,
                "label": "Title",
            },
        ),
        required=False)
    
    popuptitlecolor = forms.CharField(
       widget=ColorPalette(
            attrs={
                "label": "Title Color",
            },
        ), 
        required=False
    )
    popupmessage = forms.CharField(
        widget=TextBoxWidget(
            attrs={
                "is_color_box_display": True,
                "label": "Message",
            },
        ),
        required=False)
    
    popupmessagecolor = forms.CharField(
       widget=ColorPalette(
            attrs={
                "label": "Message Color",
            },
        ), 
        required=False
    )

    # class Meta:
    #     entangled_fields ={
    #         'glossary' : [
    #             'btn_text',
    #             'popuptitle',
    #             'popuptitlecolor',
    #             'popupmessage',
    #             'popupmessagecolor'
    #         ]
    #     }
    #     untangled_fields = []
    
class HeaderPluginForm(CascadeModelForm):

    LAYOUT_CHOICES = [
        (
            "LAYOUT1",
            _("Classic header (logo, menu, telephone number, social networks)"),
        ),
        ("LAYOUT2", _("Classic header with multiple locations and social networks")),
        (
            "LAYOUT3",
            _(
                """Classic header with products bar
                (delivery, consumer location, store name, search bar, consumer account, cart)"""
            ),
        ),
    ]
    FLOATING_MENU_CHOICES = [
        (True, _("Show")),
        (False, _("Don't show"))
    ]

    PHONENUMBER_LAYOUT_CHOICES = [
        ("ICON ONLY", _("Icon only")),
        ("ICON AND TELEPHONE NUMBER", _("Icon and telephone number")),
        ("DON’T SHOW TELEPHONE NUMBER", _("Don’t show telephone number")),
    ]

    SOCIALICON_DISPLAY_CHOICES = [
        ("SHOW", _("Show")),
        ("DON’T SHOW", _("Don’t show")),
    ]

    layout = forms.ChoiceField(
        choices=LAYOUT_CHOICES,
        label="Header's Layout",
        initial="LAYOUT1",
        help_text="Specify the layout of header section.",
        widget=forms.RadioSelect(),
    )

    background_color = forms.CharField(
        # widget=ColorWidget({"format": "hexa"}), initial="#ffffffff", required=False,
        widget=ColorPalette(),
        required=False,
    )


    element_color = forms.CharField(
        # widget=ColorWidget({"format": "hexa"}), initial="#ffffffff", required=False,
        widget=ColorPalette(
        ),
        required=False,
    )

    dropdown_item_color = forms.CharField(
        # widget=ColorWidget({"format": "hexa"}), initial="#ffffffff", required=False,
        widget=ColorPalette(
        ),
        required=False,
    )

    logo = forms.ModelChoiceField(
        queryset=ThemeImages.objects.filter(image_type="logo"),
        help_text="Select a logo to display on the header. Or add an additional one.",
    )

    locationbar_bg_color = forms.CharField(
        widget=ColorPalette(
        ),
        required=False,
    )
    locationbar_element_color = forms.CharField(
        widget=ColorPalette(
        ),
        required=False,
    )
    productbar_bg_color = forms.CharField(
        # widget=ColorWidget({"format": "hexa"}), initial="#ffffffff", required=False,
        widget=ColorPalette(),
        required=False,
    )
    productbar_element_color = forms.CharField(
        # widget=ColorWidget({"format": "hexa"}), initial="#ffffffff", required=False,
        widget=ColorPalette(
        ),
        required=False,
    )
    phonenumber_layout = forms.ChoiceField(
        choices=PHONENUMBER_LAYOUT_CHOICES,
        initial="ICON ONLY",
        widget=CustomRadioSelect(
            attrs={
                    "section_heading": "Phone Number",
                    "section_heading_desc": "How you want your telephone number to be displayed:",
                },
        ),
    )

    socialicon_display = forms.ChoiceField(
        choices=SOCIALICON_DISPLAY_CHOICES,
        initial="SHOW",
        # help_text="Specify show or dont show social icons",
        widget=CustomRadioSelect(
            attrs={
                    "section_heading": "Social Networks",
                },
        ),
    )
    is_contactus_menu = forms.ChoiceField(
        choices=FLOATING_MENU_CHOICES,
        initial="False",
        widget=CustomRadioSelect(
            attrs={
                    "section_heading": "Need Help floating button",
                },
        ),
    )
    custom_menus = forms.MultipleChoiceField(
        choices = [],
        label = "Menus",
        widget= CustomCheckBox(
            attrs={
                    "section_heading": "Menu",
                },
        ),
        required= False
    )

    button_internallink = forms.ModelChoiceField(
        blank=True,
        required=False,
        queryset=Page.objects.filter(publisher_is_draft=False),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    class Meta:
        model = HeaderPluginModel
        entangled_fields = {
            "glossary": [
                "layout",
                "background_color",
                "element_color",
                "productbar_bg_color",
                "productbar_element_color",
                "phonenumber_layout",
                "socialicon_display",
                "dropdown_item_color",
                "is_contactus_menu",
                'locationbar_bg_color',
                'locationbar_element_color',
                'custom_menus',
                "button_internallink"
            ]
        }
        untangled_fields = ["logo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        theme_object = ThemeConfiguration.objects.all()
        if theme_object:
            self.fields['productbar_bg_color'].initial = theme_object.first().primary_color
            
        queryset = Page.objects.filter(publisher_is_draft=True, in_navigation=False)
        descendant_ids = []
        for page in queryset:
            if page.is_home != True:
                descendants = page.get_descendant_pages()
                descendant_ids.extend(descendant.id for descendant in descendants )

        # links_excluded_data = Page.objects.filter(publisher_is_draft=True,title_set__published = True).exclude(id__in = descendant_ids).order_by('node__path')
        # quick_links_data = [(
        #     query.id,
        #     query.get_menu_title()
        # ) for query in links_excluded_data ]
        queryset=Page.objects.filter(publisher_is_draft=True,title_set__publisher_state = 0).order_by('node__path')
        quick_links_data = [(
            query.id,
            query.get_menu_title()
        ) for query in queryset ]
        self.fields['custom_menus'].choices = quick_links_data




class FooterPluginForm(CascadeModelForm):

    PHONENUMBER_LAYOUT_CHOICES = [
        ("ICON AND DEFAULT TEXT", _("Icon and default text ")),
        ("ICON AND TELEPHONE NUMBER", _("Icon and telephone number")),
        ("DON’T SHOW TELEPHONE NUMBER", _("Don’t show telephone number")),
    ]

    EMAIL_LAYOUT_CHOICES = [
        ("ICON AND DEFAULT TEXT", _("Icon and default text ")),
        ("ICON AND EMAIL", _("Icon and email")),
        ("DON’T SHOW EMAIL", _("Don’t show email")),
    ]

    LOCATION_LAYOUT_CHOICES = [
        ("ICON AND DEFAULT TEXT", _("Icon and default text ")),
        ("ICON AND STORE ADDRESS", _("Icon and Store Address")),
        ("DON’T SHOW ADDRESS", _("Don’t show Address")),
    ]

    SOCIALICON_DISPLAY_CHOICES = [
        ("SHOW", _("Show")),
        ("DON’T SHOW", _("Don’t show")),
    ]

    QUICKLINKS_DISPLAY_CHOICES = [
        ("SHOW", _("Show")),
        ("DON’T SHOW", _("Don’t show")),
    ]

    STOREHOURS_DISPLAY_CHOICES = [
        ("SHOW", _("Show")),
        ("DON’T SHOW", _("Don’t show")),
    ]

    background_color = forms.CharField(
        widget=ColorWidget({"format": "hexa"}),
        initial="#003f5aff",
    )

    element_color = forms.CharField(
        widget=ColorWidget({"format": "hexa"}),
        initial="#ffffffff",
    )

    logo = forms.ModelChoiceField(
        queryset=ThemeImages.objects.filter(image_type="logo"),
        help_text="Select a logo to display on the footer. Or add an additional one.",
    )
    
    first_location = forms.ChoiceField(
        label="Location",
        help_text="Select a locations to display first contact us detail.",
        widget=forms.Select(),
        required=False,
    )
    
    second_location = forms.ChoiceField(
        label="Location",
        help_text="Select a locations to display first contact us detail.",
        widget=forms.Select(),
        required=False,
    )

    phonenumber_layout = forms.ChoiceField(
        choices=PHONENUMBER_LAYOUT_CHOICES,
        label="Phonenumber's Layout",
        initial="ICON AND DEFAULT TEXT",
        help_text="How you want your telephone number to be displayed",
        widget=forms.RadioSelect(),
    )

    email_layout = forms.ChoiceField(
        choices=EMAIL_LAYOUT_CHOICES,
        label="Email's Layout",
        initial="ICON AND DEFAULT TEXT",
        help_text="How you want your email address to be displayed",
        widget=forms.RadioSelect(),
    )

    location_layout = forms.ChoiceField(
        choices=LOCATION_LAYOUT_CHOICES,
        label="Location's Layout",
        initial="ICON AND DEFAULT TEXT",
        help_text="How you want your store location to be displayed",
        widget=forms.RadioSelect(),
    )

    socialicon_display = forms.ChoiceField(
        choices=SOCIALICON_DISPLAY_CHOICES,
        label="Social icon display",
        initial="SHOW",
        help_text="Specify show or dont show social icons.",
        widget=forms.RadioSelect(),
    )

    quicklinks_display = forms.ChoiceField(
        choices=QUICKLINKS_DISPLAY_CHOICES,
        label="Quick links display",
        initial="SHOW",
        help_text="Quick links will be provided in accordance with main menu on the header.",
        widget=forms.RadioSelect(),
    )

    storehours_display = forms.ChoiceField(
        choices=STOREHOURS_DISPLAY_CHOICES,
        label="Store hours display",
        initial="SHOW",
        help_text="Specify show or dont show store hours.",
        widget=forms.RadioSelect(),
    )
    quick_links = forms.MultipleChoiceField(
        choices = [],
        label = "Quick Links",
        widget= CustomCheckBox(),
        required= False
    )
    external_quick_links = forms.CharField()

    class Meta:
        model = FooterPluginModel
        entangled_fields = {
            "glossary": [
                "background_color",
                "element_color",
                "first_location",
                "second_location",
                "phonenumber_layout",
                "email_layout",
                "location_layout",
                "socialicon_display",
                "quicklinks_display",
                "storehours_display",
                "quick_links",
            ]
        }
        untangled_fields = ["logo", "external_quick_links"]
    
    def __init__(self, *args, **kwargs):
        super(FooterPluginForm, self).__init__(*args, **kwargs)
        self.client = PWAPI()
        
        # Fetch pet locations from pos
        locations_list = [
            (location["id"], location["entity"]["name"])
            for location in get_stores_data(client=self.client)
        ]
        locations_list.insert(0, ("", "Default"))

        self.fields["first_location"].choices = locations_list
        self.fields["second_location"].choices = locations_list

        queryset=Page.objects.filter(publisher_is_draft=True,title_set__publisher_state = 0).order_by('node__path')
        quick_links_data = [(
            query.id,
            query.get_menu_title()
        ) for query in queryset]
        self.fields['quick_links'].choices = quick_links_data
        


class InfoBlockFirstPluginForm(CascadeModelForm):

    LAYOUT_CHOICES = [
        ("LAYOUT1", _("Square image left side, Content right side")),
        ("LAYOUT2", _("Square image right side, Content left side")),
        ("LAYOUT3", _("Round image left side, Content right side")),
        ("LAYOUT4", _("Round image right side, Content left side")),
        ("LAYOUT5", _("Full image right side, Content left side")),
        ("LAYOUT6", _("Full image right side, Content left side with form")),
        ("LAYOUT7", _("Full image left side, Content right side")),
        ("LAYOUT8", _("Image full screen wide and text on the left")),
        ("LAYOUT9", _("Image full screen wide and text on the right")),
        ("LAYOUT10", _("Image full screen wide and text centered")),
        ("LAYOUT11", _("Image full screen wide only")),
    ]
    LAYOUT_CHOICES2 = [
        ('LAYOUT12', _('Images left and right and text centered')),
    ]
    VIDEO_LAYOUT = [
        ('LAYOUT13', _('Video left and text on the right')),
        ('LAYOUT14', _('Text left and video on the right ')),
        ('LAYOUT15', _('Video and text centered')),
        ('LAYOUT16', _('Video only')),
    ]

    BUTTON_STYLE = [
        ("fill", _("Fill")),
        ("outline", _("Outline")),
    ]

    BG_TYPE_CHOICES = [
        ("image", _("Image")),
        ("color", _("Color")),
        
    ]
    BACKGROUND = [
        ("yes", _("Yes")),
        ("no",_('No'))
    ]

    layout = forms.ChoiceField(
        choices=LAYOUT_CHOICES,
        label="Info block's Layout",
        initial="LAYOUT1",
        help_text="Specify the layout of info block.",
        widget=forms.RadioSelect(),
    )
    layout2 = forms.ChoiceField(
        choices=LAYOUT_CHOICES2,
        label="Info block's Layout",
        initial="LAYOUT12",
        help_text="Specify the layout of info block2.",
        widget=forms.RadioSelect(),
        required=False
    )
    layout_video = forms.ChoiceField(
        choices=VIDEO_LAYOUT,
        label="Info block's Layout",
        initial="LAYOUT13",
        help_text="Specify the layout of info block.",
        widget=forms.RadioSelect(),
        required=False
    )
    
    bg_color = forms.CharField(
        required=False,
        widget=ColorPalette(),
    )

    image = forms.ImageField(
        label="Upload Image",
        help_text="Upload your .JPG, .PNG, .SVG, .WEBP or .GIF files here.",
        required=False
    )
    alt_name_image = forms.CharField(required=False,widget=TextBoxWidget(
        attrs= { 
            "is_color_box_display": False,
            "placeholder": "Enter ALT text",
            }
    ))
    mobimage = forms.ImageField(
        label="Upload Image",
        help_text="Upload your .JPG, .PNG, .SVG, .WEBP or .GIF files here.",
        required=False
    )
    alt_name_mobimage = forms.CharField(required=False,widget=TextBoxWidget(
        attrs= { 
            "is_color_box_display": False,
            "placeholder": "Enter ALT text",
            }
    ))
    bg_image = forms.ImageField(
        label="Upload Background Image",
        help_text="Upload your .JPG, .PNG, .SVG, .WEBP or .GIF files here.",
        required=False,
    )
    alt_name_bg_image = forms.CharField(required=False,widget=TextBoxWidget(
        attrs= { 
            "is_color_box_display": False,
            "placeholder": "Enter ALT text",
            }
    ))
    image_left = forms.ImageField(
        label="On the left side",
        help_text="Upload your .JPG, .PNG, .SVG, .WEBP or .GIF files here.",
        required=False,
    )

    alt_name_image_left = forms.CharField(required=False,widget=TextBoxWidget(
        attrs= { 
            "is_color_box_display": False,
            "placeholder": "Enter ALT text",
            }
    ))

    image_right = forms.ImageField(
        label="On the right side",
        help_text="Upload your .JPG, .PNG, .SVG, .WEBP or .GIF files here.",
        required=False,
    )
    
    alt_name_image_right = forms.CharField(required=False,widget=TextBoxWidget(
        attrs= { 
            "is_color_box_display": False,
            "placeholder": "Enter ALT text",
            }
    ))

    video = forms.FileField(required=False, validators=[FileExtensionValidator(['mp4', 'avi', 'mov'])], widget=FileInput(attrs={'class': 'custom-file-input'}))

    title_text = forms.CharField(required=False,widget=CKEditorTextboxWidget(
        attrs={ 
            "placeholder": "Enter title",
             "section_heading_desc" : "Recommended text format – H2.",
             "toolbars" : [ 'undo', 'redo', '|', 'fontFamily', 'fontSize','|', 'fontColor', 'fontBackgroundColor','|','bold', 'italic', 'underline','strikethrough', '|',
            'link', 'uploadImage', 'blockQuote', '|',
            'alignment',
            'sourceEditing'
            ],
            "fontSize" : [24,40],
            "paragraph" : False,
            "fontFamily" : []
            }
    ))

    title_text_color = forms.CharField(
        widget=ColorPalette(attrs= {
          "label" : "Font Color",
        }), initial="#000000ff", required=False
    )
    sub_title_text = forms.CharField(required=False,widget=CKEditorTextboxWidget(
        attrs={ 
            "placeholder": "Enter title",
             "label" : "Sub title",
             "toolbars" : ['fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'highlight', '|','alignment', '|', 'heading'],
            "heading" : ['1','4','5'],
            "fontSize" : [ 4 ,5 ,12, 23],
            "paragraph" : True
            }
    ))

    sub_title_text_color = forms.CharField(
        widget=ColorPalette(attrs= {
            'label' : 'Font Color',
        }), initial="#000000ff", required=False
    )

    message_text = forms.CharField(required=False,widget=CKEditorTextboxWidget(
        attrs={ 
            "placeholder": "Enter Message",
             'section_heading_desc' : 'Recommended text size– 18.',
            }
    ))

    bg_type = forms.ChoiceField(
        choices=BG_TYPE_CHOICES,
        label="Type",
        initial="image",
        help_text="Specify the type of background",
        widget=CustomRadioSelect(
            attrs={
                'horizontal_layout': True,
            }
        ),
    )

    
    isdescription=forms.ChoiceField(
        choices=ISBUTTON_CHOICES,
        label="Handle button visibility",
        initial="True",
        help_text="Handle button visibility",
        widget=forms.RadioSelect())

    message_text_color = forms.CharField(
        widget=ColorPalette(attrs={
            "label" : "Font Color",
        }), initial="#000000ff", required=False,
    )

    button_text = forms.CharField(required=False)

    button_link = forms.URLField(required=False)

    button_internallink = forms.ModelChoiceField(
        blank=True,
        required=False,
        queryset=Page.objects.filter(publisher_is_draft=False),
    )

    BUTTON_TARGET_CHOICES = [
        ("_self", _("Same Window"),),
        ("_blank", _("New Window"),),
    ]
    button_target = forms.ChoiceField(
        choices=BUTTON_TARGET_CHOICES,
        label="BUTTON_TARGET",
        initial="_self",
        help_text="Specify the target of button.",
        widget=forms.Select(),
        required=False,
    )

    button_style = forms.ChoiceField(
        choices=BUTTON_STYLE, initial="fill", required=False
    )

    button_fill_color = forms.CharField(
        widget=ColorWidget({"format": "hexa"}), initial="#ffffffff", required=False
    )

    button_font_color = forms.CharField(
        widget=ColorWidget({"format": "hexa"}), initial="#000000ff", required=False
    )

    button_outline_color = forms.CharField(
        widget=ColorWidget({"format": "hexa"}), initial="#000000ff", required=False
    )
    mytext = forms.CharField(required=False)
    QUANTITY_OF_IMG = [
        ("QTY1", _("1"),),
        ("QTY2", _("2"),),
    ]
    quantity_of_image = forms.ChoiceField(
        choices=QUANTITY_OF_IMG,
        help_text="Quantity of images",
        initial= "QTY1",
        widget=CustomRadioSelect(
            attrs={
                'horizontal_layout': True,
            }
           
        ),
        required=False
    )
    MEDIA_TYPE = [
        ("Image", _("Image"),),
        ("Video", _("Video"),),
        ("None", _("None"),),
    ]
    media_type = forms.ChoiceField(
        choices=MEDIA_TYPE,
        help_text="Media",
        initial="Image",
        widget=CustomRadioSelect(
            attrs={
                'horizontal_layout': True,
            }
           
        ),
        required=False
    )
    VIDEO_TYPE = [
        ("link", _("Link"),),
        ("upload", _("Upload"),),
    ]
    video_type = forms.ChoiceField(
        choices=VIDEO_TYPE,
        help_text="Video",
        initial= "upload",
        widget=CustomRadioSelect(
            attrs={
                'horizontal_layout': True,
            }
           
        ),required=False
    )

    video_link = forms.CharField(widget=TextBoxWidget(
        attrs= { 
            "is_color_box_display": False,
            "placeholder": "https://",
            "section_heading_desc" : "Provide a Vimeo or YouTube link of your video.",
            }
    ),required=False)

    button_internallink_1 = forms.ModelChoiceField(
        blank=True,
        required=False,
        queryset=Page.objects.filter(publisher_is_draft=False),
    )

    button_data = forms.CharField()

    background = forms.ChoiceField(
        choices=BACKGROUND,
        label="Type",
        initial="yes",
        help_text="Specify the type of background",
        widget=CustomRadioSelect(
            attrs={
                'horizontal_layout': True,
            }
        ),
    )

    '''
    BELOW FIELDS IS FOR COLLECTION FORM
    '''
    collection_form_title = forms.CharField(
        widget=TextBoxWidget(
            attrs={
                "is_color_box_display": True,
                "label": "Title",
            },
        ),
        required=False)
    
    collection_form_subtitle = forms.CharField(
        widget=TextBoxWidget(
            attrs={
                "is_color_box_display": True,
                "label": "Subtitle",
            },
        ),
        required=False)
    
    collection_form_title_color = forms.CharField(
        widget=ColorPalette(
            attrs={
                "label": "Font Color",
            }
        ),
        required=False,
    )
    collection_form_subtitle_color = forms.CharField(
        widget=ColorPalette(
            attrs={
                "label": "Font Color",
            }
        ),
        required=False,
    )
    collection_form_btn=forms.ChoiceField(
        choices=BUTTON_STYLE, initial="fill", required=False
    )
    '''
    END COLLECTION FORM
    '''
    class Meta:
        model = InfoBlockFirstPluginModel
        entangled_fields = {
            "glossary": [
                'collection_form_title',
                'collection_form_subtitle',
                'collection_form_title_color',
                'collection_form_subtitle_color',
                'collection_form_btn',
                "layout",
                "bg_color",
                "title_text",
                "title_text_color",
                "sub_title_text",
                "sub_title_text_color",
                "message_text",
                "message_text_color",
                "button_text",
                "button_link",
                "button_internallink",
                "button_style",
                "button_fill_color",
                "button_font_color",
                "button_outline_color",
                "isdescription",
                "bg_type",
                "button_target",
                'mytext',
                'quantity_of_image',
                'media_type',
                'layout2',
                'layout_video',
                "alt_name_image",
                "alt_name_mobimage",
                "alt_name_bg_image",
                "alt_name_image_left",
                "alt_name_image_right",
                "video_type",
                "video_link",
                "button_internallink_1",
                "background",
            ]
        }
        untangled_fields = ["image", "mobimage", "video","bg_image","image_left","image_right", "button_data"]


class InfoBlockSecondPluginForm(CascadeModelForm):

    BUTTON_STYLE = [
        ("fill", _("Fill")),
        ("outline", _("Outline")),
    ]

    image_left = forms.ImageField(
        label="Upload Image",
        help_text="Upload your .JPG, .PNG, .SVG, .WEBP or .GIF files here.",
    )

    image_right = forms.ImageField(
        label="Upload Image",
        help_text="Upload your .JPG, .PNG, .SVG, .WEBP or .GIF files here.",
    )

    title_text = forms.CharField(required=False)

    title_text_color = forms.CharField(
        widget=ColorWidget({"format": "hexa"}), initial="#000000ff", required=False
    )

    sub_title_text = forms.CharField(required=False)

    sub_title_text_color = forms.CharField(
        widget=ColorWidget({"format": "hexa"}), initial="#000000ff", required=False
    )

    message_text = forms.CharField(required=False)

    message_text_color = forms.CharField(
        widget=ColorWidget({"format": "hexa"}), initial="#000000ff", required=False
    )

    isbutton=forms.ChoiceField(
        choices=ISBUTTON_CHOICES,
        label="Handle button visibility",
        initial="True",
        help_text="Handle button visibility",
        widget=forms.RadioSelect())

    button_text = forms.CharField(required=False)

    button_link = forms.URLField(required=False)

    button_internallink = forms.ModelChoiceField(
        blank=True,
        required=False,
        queryset=Page.objects.filter(publisher_is_draft=False),
    )

    button_style = forms.ChoiceField(
        choices=BUTTON_STYLE, initial="fill", required=False
    )

    button_fill_color = forms.CharField(
        widget=ColorWidget({"format": "hexa"}), initial="#ffffffff", required=False
    )

    button_font_color = forms.CharField(
        widget=ColorWidget({"format": "hexa"}), initial="#000000ff", required=False
    )

    button_outline_color = forms.CharField(
        widget=ColorWidget({"format": "hexa"}), initial="#000000ff", required=False
    )

    class Meta:
        model = InfoBlockSecondPluginModel
        entangled_fields = {
            "glossary": [
                "title_text",
                "title_text_color",
                "sub_title_text",
                "sub_title_text_color",
                "message_text",
                "message_text_color",
                "button_text",
                "button_link",
                "button_internallink",
                "button_style",
                "button_fill_color",
                "button_font_color",
                "button_outline_color",
                'isbutton'
            ]
        }
        untangled_fields = ["image_left", "image_right"]


class SliderPluginForm(CascadeModelForm):

    SLIDER_OPTION_CHOICES = [
        ("true", _("Show")),
        ("false", _("Don’t show")),
    ]

    SLIDER_LOOP_CHOICES = [
        ("true", _("True")),
        ("false", _("False")),
    ]

    arrow_display = forms.ChoiceField(
        choices=SLIDER_OPTION_CHOICES,
        label="Navigation arrow display",
        initial="true",
        help_text="Choose whether to display navigation arrows.",
        widget=forms.RadioSelect(),
    )

    dots_display = forms.ChoiceField(
        choices=SLIDER_OPTION_CHOICES,
        label="Navigation dots display",
        initial="true",
        help_text="Choose whether to display dots below the slider.",
        widget=forms.RadioSelect(),
    )

    slider_loop = forms.ChoiceField(
        choices=SLIDER_LOOP_CHOICES,
        label="Looping",
        initial="true",
        help_text="Choose whether the slider should loop continuously or stop at the last slide.",
        widget=forms.RadioSelect(),
    )

    slider_autoplay = forms.ChoiceField(
        choices=SLIDER_LOOP_CHOICES,
        label="Autoplay",
        initial="false",
        help_text="Set the slider to play automatically or not.",
        widget=forms.RadioSelect(),
    )

    class Meta:
        model = SliderPluginModel
        entangled_fields = {
            "glossary": [
                "arrow_display",
                "dots_display",
                "slider_loop",
                "slider_autoplay",
            ]
        }
        untangled_fields = []

class StaticInfoBlockItemForm(CascadeModelForm):
    """
    Store data of individual item of static info block plugin
    """

    item_title = forms.CharField(required=False)
    
    image_file = CascadeImageField()

    url=forms.CharField(required=False)
    
    button_internallink = forms.ModelChoiceField(
        blank=True,
        required=False,
        queryset=Page.objects.filter(publisher_is_draft=False),
    )

    class Meta:
        entangled_fields = {
            "glossary": [
                "item_title",
                "url",
                "image_file",
                'button_internallink'
            ]
        }
        untangled_fields = []


class StaticInfoItemInline(StackedInline):
    """
    Inline form in static info block plugin
    """
    
    model = InlineCascadeElement
    form = StaticInfoBlockItemForm
    raw_id_fields = ['image_file']
    verbose_name = _("Static Info Item")
    verbose_name_plural = _("Static Info Items")
    extra = 1



class StaticInfoBlockPluginForm(CascadeModelForm):
    """
    Store data of static info block
    """

    info_title = forms.CharField(required=False)

    bg_color = forms.CharField(
        widget=ColorWidget({"format": "hexa"}), initial="#ffffffff", required=False
    )

    info_title_color = forms.CharField(
        widget=ColorWidget({"format": "hexa"}), initial="#000000ff", required=False
    )

    item_title_color = forms.CharField(
        widget=ColorWidget({"format": "hexa"}), initial="#000000ff", required=False
    )

    item_outer_color = forms.CharField(
        widget=ColorWidget({"format": "hexa"}), initial="#000000ff", required=False
    )

    columns_to_display = forms.CharField(initial="3", required=False)

    STATIC_BLOCK_BUTTON_CHOICES = [
    (True, _("Show")),
    (False, _("Hide"))
    ]

    isbutton = forms.ChoiceField(
        choices=STATIC_BLOCK_BUTTON_CHOICES,
        label="Handle button visibility",
        initial="True",
        widget=forms.RadioSelect())

    button_text = forms.CharField(required=False)

    main_button_link = forms.URLField(required=False)

    main_button_internallink = forms.ModelChoiceField(
        blank=True,
        required=False,
        queryset=Page.objects.filter(publisher_is_draft=False),
    )

    BUTTON_STYLE = [
        ("fill", _("Fill")),
        ("outline", _("Outline")),
    ]

    button_style = forms.ChoiceField(
        choices=BUTTON_STYLE, initial="fill", required=False
    )     

    class Meta:
        entangled_fields = {
            "glossary": [
                "info_title",
                "bg_color",
                "info_title_color",
                "item_title_color",
                "item_outer_color",
                "columns_to_display",
                "isbutton",
                "button_text",
                "main_button_link",
                "main_button_internallink",
                "button_style"
            ]
        }
        untangled_fields = []


class SubscribeUsPluginForm(CascadeModelForm):
    """
    Store data of Subscribe us plugin
    """
    MARKETINGLIST = [
        ('Email', 'Promotional (Email)'),
        ('Email', 'Newsletter (Email)'),
        ('SMS', 'Promotional (SMS)'),
    ]
    MARKETING_LAYOUT_CHOICES_EMAIL = [
        ("LAYOUT1", _("No image, collection form only")),
        ("LAYOUT2", _("No image, collection form centered")),
        ("LAYOUT3", _("Image right and collection form on the left")),
        ("LAYOUT4", _("Image left and collection form on the right")),
        ("LAYOUT5", _("Two images and a collection form")),
    ]
    MARKETING_LAYOUT_CHOICES_SMS = [
        ("LAYOUT6", _("No image, collection form only")),
        ("LAYOUT7", _("No image, collection form centered")),
        ("LAYOUT8", _("Image right and collection form on the left")),
        ("LAYOUT9", _("Image left and collection form on the right")),
        ("LAYOUT10", _("Two images and a collection form")),
    ]
    BACKGROUND = [
        ("yes", _("Yes")),
        ("no",_('No'))
    ]
    BACKGROUND_TYPE = [
        ("Image", _("Image")),
        ("Color",_('Color'))
    ]
    BUTTON_STYLE = [
        ("fill", _("Fill")),
        ("outline", _("Outline")),
    ]
    marketing_list = forms.ChoiceField(
       
        choices = MARKETINGLIST,
        initial="Email",
        widget= CustomRadioSelect(
        ),
    )
    marketing_layouts_email = forms.ChoiceField(
        choices=MARKETING_LAYOUT_CHOICES_EMAIL,
        initial="LAYOUT1",
        widget=CustomRadioSelect(),
    )
    marketing_layouts_sms = forms.ChoiceField(
        choices=MARKETING_LAYOUT_CHOICES_SMS,
        initial="LAYOUT6",
        widget=CustomRadioSelect(),
    )

    background = forms.ChoiceField(
        choices=BACKGROUND,
        initial="yes",
        widget=CustomRadioSelect(
            attrs={
                'horizontal_layout': True,
            }
        ),
    )
    background_type = forms.ChoiceField(
        choices=BACKGROUND_TYPE,
        initial="Image",
        widget=CustomRadioSelect(
            attrs={
                'horizontal_layout': True,
            }
        ),
    )

    marketing_message = forms.CharField(widget=CKEditorTextboxWidget(
        attrs={ 
            "placeholder": "Write message here",
            }
    ),required=False)
    
    marketing_font_color = forms.CharField(
        widget=ColorPalette(
            attrs={
                "section_heading_desc" : "Font color"
            }
        ),
        required=False,
    )

    marketing_button_text = forms.CharField(required=False,
        initial="Submit",
        widget=TextBoxWidget(
        attrs= { 
            "is_color_box_display": False,
            }
    ))

    marketing_button_style = forms.ChoiceField(
        # widget=CustomButtonStyle(
        # ),
        choices=BUTTON_STYLE, initial="fill", required=False
    )
    marketing_button_color = forms.CharField(
        required=False)

    title = forms.CharField(max_length=55, required=False)

    sub_title = forms.CharField(
                    max_length=255, required=False, 
                    initial="Subscribe now and be the first to know on our new arrivals"
                )

    newsletter_bg_image = forms.ImageField(
        label="Upload Image",
        help_text="Upload your .JPG, .PNG, .SVG, .WEBP or .GIF files here.",
        required=False
    )
    newsletter_image = forms.ImageField(
        label="Upload Image",
        help_text="Upload your .JPG, .PNG, .SVG, .WEBP or .GIF files here.",
        required=False
    )
    alt_newsletter_image = forms.CharField(required=False,widget=TextBoxWidget(
        attrs= { 
            "is_color_box_display": False,
            "placeholder": "Enter ALT text",
            }
    ))
    newsletter_left_image = forms.ImageField(
        label="Upload Image",
        help_text="Upload your .JPG, .PNG, .SVG, .WEBP or .GIF files here.",
        required=False
    )
    alt_newsletter_left_image = forms.CharField(required=False,widget=TextBoxWidget(
        attrs= { 
            "is_color_box_display": False,
            "placeholder": "Enter ALT text",
            }
    ))
    newsletter_right_image = forms.ImageField(
        label="Upload Image",
        help_text="Upload your .JPG, .PNG, .SVG, .WEBP or .GIF files here.",
        required=False
    )
    alt_newsletter_right_image = forms.CharField(required=False,widget=TextBoxWidget(
        attrs= { 
            "is_color_box_display": False,
            "placeholder": "Enter ALT text",
            }
    ))
    alt_name_bg_image = forms.CharField(required=False,widget=TextBoxWidget(
        attrs= { 
            "is_color_box_display": False,
            "placeholder": "Enter ALT text",
            }
    ))
    bg_color = forms.CharField(
        initial="#ffffffff", required=False,
        widget=ColorPalette(
            attrs={
                "label": "Background Color",
            },
        ),
    )
    bg_image = CascadeImageField(required=False, label="Background image")
    
    display_default_image = forms.BooleanField(required=False, initial=True, help_text="Display default image if side image is not available.")
    
    display_text_left = forms.BooleanField(required=False, initial=False, help_text="Display Title and subtitle to the left it will not display side image.")
    
    side_image = CascadeImageField(required=False, label="Side image")

    class Meta:
        model = SubscribePluginModel
        entangled_fields = {
            "glossary": [
                "title",
                "sub_title",
                "bg_image",
                "display_default_image",
                "display_text_left",
                "side_image",
                "marketing_list",
                "marketing_layouts_email",
                "marketing_layouts_sms",
                "background",
                "background_type",
                "marketing_message",
                "marketing_font_color",
                "marketing_button_text",
                "marketing_button_style",
                "marketing_button_color",
                "bg_color",
                'alt_newsletter_image',
                'alt_newsletter_left_image',
                'alt_newsletter_right_image'
            ]
        }
        untangled_fields = ['newsletter_image','newsletter_left_image','newsletter_right_image','newsletter_bg_image']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # marketing list from api 
        client = EntityClient()
        marketingList = client.get_marketing_lists()
        marketingList = [(data['id'],data['name']) for data in marketingList.get('objects', {})]
        self.fields['marketing_list'].choices = marketingList
        if marketingList:
            self.initial['marketing_list'] = marketingList[0][0] 

class UnSubscribeUsPluginForm(CascadeModelForm):
    title = message = forms.CharField(
        required=False,
        widget=TextBoxWidget(
            attrs={
                "placeholder": "Enter Title",
                "label": "Title",
            }
        ),
    )

    sub_title = forms.CharField(
        required=False,
        widget=TextBoxWidget(
            attrs={
                "placeholder": "Enter Sub Title",
                "label": "Sub Title",
            }
        ),
    )

    class Meta:
        model = UnSubscribePluginModel
        entangled_fields = {
            "glossary": [
                "title",
                "sub_title",
            ]
        }


class CustomerVerificationForm(forms.Form):
    """
    Store data of Subscribe us plugin
    """

    first_name = forms.CharField(label=_("First Name"), max_length=55, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'})
    )
    last_name = forms.CharField(label=_("Last Name"), max_length=55, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'})
    )
    email = forms.EmailField(label=_("Email"), required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'})
    )
    phone= forms.CharField(label=_("Phone Number"), max_length=14, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Phone number', 'class': 'form-control'}),
    )

    location_id = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)

    def __init__(self, *args, **kwargs):
        super(CustomerVerificationForm, self).__init__(*args, **kwargs)

class OtpVerificationForm(forms.Form):
    """
    Store data of Subscribe us plugin
    """

    code =  forms.CharField(widget=forms.HiddenInput(), max_length=55, required=True)
    location_id = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)

    def __init__(self, *args, **kwargs):
        super(OtpVerificationForm, self).__init__(*args, **kwargs)

class ContactUsForm(forms.Form):

    first_name = forms.CharField(label=_("First Name"), max_length=55, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'aria-label': 'First Name', 'autocomplete': 'given-name'})
    )
    last_name = forms.CharField(label=_("Last Name"), max_length=55, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'aria-label': 'Last Name', 'autocomplete': 'given-name'})
    )
    email = forms.EmailField(label=_("Email"), required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'aria-label': 'Email', 'autocomplete': 'email'})
    )
    phone_number = forms.CharField(label=_("Phone Number"), max_length=14, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Phone number', 'aria-label': 'Phone Number', 'autocomplete': 'tel'}),
    )
    message = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 4, 'placeholder': 'Enter message here', 'aria-label': 'message', 'autocomplete': 'given-name'}
    ))
    form_type = forms.CharField(max_length=55, required=True)
    # captcha = ReCaptchaField()


class CollectionForm(forms.Form):
    
    first_name = forms.CharField(label=_("First Name"), max_length=55, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control', 'aria-label': 'First Name Input Field', 'autocomplete': 'given-name'})
    )
    last_name = forms.CharField(label=_("Last Name"), max_length=55, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control', 'aria-label': 'Last Name Input Field', 'autocomplete': 'given-name'})
    )
    email = forms.EmailField(label=_("Email"), required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control', 'aria-label': 'Email Input Field', 'autocomplete': 'email'})
    )
    phone = forms.CharField(label=_("Phone Number"), max_length=17, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Phone number', 'class': 'form-control phone-validation', 'aria-label': 'Phone Number Input Field', 'autocomplete': 'tel'}),
    )
    message = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 5, 'placeholder': 'Enter message here', 'class': 'form-control focus-color', 'aria-label': 'Message Input Field', 'autocomplete': 'given-name'}
    ), required=False)
    zip = forms.CharField(label=_("Zip"), max_length=12, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Zip', 'class': 'form-control', 'aria-label': 'Zip Code Input Field', 'autocomplete': 'postal-code'}),
    )

    LEAD_CHOICES = [
        ('Adopt', 'Adopt'),
        ('Breeder', 'Breeder'),
    ]
    lead_type = forms.ChoiceField(
        label=_("Lead Type"),
        choices=LEAD_CHOICES,
        widget=forms.Select(attrs={'placeholder': 'Are you looking to adopt or a breeder?', 'class': 'form-control'}),
        required=False
    )

    location_id = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    location = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False) # name

    pet_id = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    pet_gender = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)

    breed = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False) # name 
    breed_slug = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)

    breed_pet_type_slug = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    pet_type_slug = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)

    
    email_me_more = forms.BooleanField(required=False)
    sms_okay = forms.BooleanField(required=False)
    shop_window = forms.BooleanField(required=False)
    form = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=True)
    site_url = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=True)
    page_referer = forms.CharField(widget=forms.HiddenInput(), max_length=100, required=True)

    captcha = ReCaptchaField(error_messages = {'required': "Captcha is required"})
    
    def __init__(self, *args, **kwargs):
        super(CollectionForm, self).__init__(*args, **kwargs)


class SubscribeUsForm(forms.Form):
    
    first_name = forms.CharField(label=_("First Name"), max_length=55, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control', 'aria-label': 'First Name', 'autocomplete': 'given-name'})
    )
    last_name = forms.CharField(label=_("Last Name"), max_length=55, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control', 'aria-label': 'Last Name', 'autocomplete': 'given-name'})
    )
    phone = forms.CharField(label=_("Your telephone number"), max_length=13, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Your telephone number', 'class': 'form-control', 'aria-label': 'Phone Number', 'autocomplete': 'tel'})
    )
    email = forms.EmailField(label=_("Your Email"), required=False,
        widget=forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-control', 'aria-label': 'Email', 'autocomplete': 'email'})
    )
    
    breed_name = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    breed_pet_type_slug = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    pet_type_slug = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    pet_id = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    location_id = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    message = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    
    email_me_more = forms.CharField(initial=1, widget=forms.HiddenInput())
    sms_okay = forms.CharField(initial=0, widget=forms.HiddenInput())
    form = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=True)
    shop_window = forms.BooleanField(required=False)
    captcha = ReCaptchaField(error_messages = {'required': "Captcha is required"})
    
    def __init__(self, *args, **kwargs):
        super(SubscribeUsForm, self).__init__(*args, **kwargs)

class AvailablePuppyCollectionForm(forms.Form):

    name = forms.CharField(label=_("First Name"), max_length=55, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First and Last Name', 'class': 'form-control'})
    )
    email = forms.EmailField(label=_("Email"), required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'})
    )
    
    breed_name = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    breed_pet_type_slug = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    pet_type_slug = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    pet_id = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    location_id = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    message = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    
    email_me_more = forms.CharField(initial=1, widget=forms.HiddenInput())
    sms_okay = forms.CharField(initial=0, widget=forms.HiddenInput())
    form = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=True)
    captcha = ReCaptchaField(error_messages = {'required': "Captcha is required"})
    
    def __init__(self, *args, **kwargs):
        super(AvailablePuppyCollectionForm, self).__init__(*args, **kwargs)

class FranchiseCollectionForm(forms.Form):
    
    first_name = forms.CharField(label=_("First Name"), max_length=55, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'})
    )
    last_name = forms.CharField(label=_("Last Name"), max_length=55, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'})
    )
    email = forms.EmailField(label=_("Email"), required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'})
    )
    phone = forms.CharField(label=_("Phone Number"), max_length=17, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Phone number', 'class': 'form-control phone-validation'}),
    )
    # additional_information= forms.CharField(widget=forms.Textarea(
    #     attrs={'rows': 3, 'placeholder': 'Enter message here', 'class': 'form-control'}
    # ))

    zip = forms.CharField(label=_("zip"), max_length=12, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'ZIP', 'class': 'form-control'}),
    )
    # capital_availabe = forms.CharField(label=_("Capital Availabe"), max_length=12, required=True,
    #     widget=forms.TextInput(attrs={'placeholder': 'Capital Availabe', 'class': 'form-control'}),
    # )
    # Timeline = forms.CharField(label=_("Timeline"), max_length=12, required=True,
    #     widget=forms.TextInput(attrs={'placeholder': 'Timeline', 'class': 'form-control'}),
    # )
    # pet_id = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    
    email_me_more = forms.BooleanField(required=False)
    sms_okay = forms.BooleanField(required=False)
    form = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=True)
    # captcha = ReCaptchaField(error_messages = {'required': "Captcha is required"})
    
    def __init__(self, *args, **kwargs):
        super(FranchiseCollectionForm, self).__init__(*args, **kwargs)

class SchedulePlaydate(forms.Form):
    
    first_name = forms.CharField(label=_("First Name"), max_length=55, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control', 'aria-label': 'First Name', 'autocomplete': 'given-name'})
    )
    last_name = forms.CharField(label=_("Last Name"), max_length=55, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control', 'aria-label': 'Last Name', 'autocomplete': 'given-name'})
    )
    email = forms.EmailField(label=_("Email"), required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control', 'aria-label': 'Email', 'autocomplete': 'email'})
    )
    phone = forms.CharField(label=_("Phone Number"), max_length=17, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Phone number', 'class': 'form-control phone-validation', 'aria-label': 'Phone Number', 'autocomplete': 'tel'}),
    )
    pet_type_slug = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    pet_id = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=False)
    form = forms.CharField(widget=forms.HiddenInput(), max_length=55, required=True)
    captcha = ReCaptchaField()
    
    def __init__(self, *args, **kwargs):
        super(SchedulePlaydate, self).__init__(*args, **kwargs)

class GalleryItemForm(CascadeModelForm):
    """
    Store data of individual image of gallery plugin
    """

    SQUARE_IMAGE = 'Square'
    DOUBLE_IMAGE = 'Double Wide'

    image_size_choices = (
        (SQUARE_IMAGE, SQUARE_IMAGE),
        (DOUBLE_IMAGE, DOUBLE_IMAGE),
    )

    image_title = forms.CharField(
        required=False,
        widget=TextBoxWidget(
            attrs={
                "section_sub_heading": "Title",
                "input_type": "text",
                "placeholder": "Enter Title",
            }
        ),
    )

    image_label = forms.CharField(
        required=False,
        widget=TextBoxWidget(
            attrs={
                "section_sub_heading": "Label",
                "input_type": "text",
                "placeholder": "Enter Label",
            }
        ),
    )
    image_size = forms.ChoiceField(
        choices=image_size_choices,
        initial=SQUARE_IMAGE,
        widget=CustomRadioSelect(
            attrs={
                    "section_sub_heading": "Card Size",
                    "horizontal_layout": True,
                },
        ),
    )
    image_url = forms.CharField(
        required=False,
        widget=LinkWidget(
            ajax_view="admin:cms_page_get_published_pagelist",
            attrs = {
                "label": "Internal/External Link",
                "placeholder": "Start typing...",
            }
        ),
    )
    image_file = CascadeImageField()

    class Meta:
        entangled_fields = {
            "glossary": [
                "image_title",
                "image_label",
                "image_size",
                "image_url",
                "image_file",
            ]
        }
        untangled_fields = []


class GalleryPluginForm(CascadeModelForm):
    """
    Store data of Gallery Plugin
    """

    ACTION_LINK = "Link"
    ACTION_LARGE_IMAGE = "Large Image"
    LABEL_BG_SOLID = "Solid"
    LABEL_BG_GRADIENT = "Gradient"

    action_choices = (
        (ACTION_LINK, ACTION_LINK),
        (ACTION_LARGE_IMAGE, ACTION_LARGE_IMAGE),
    )

    label_bg_style_choices = (
        (LABEL_BG_SOLID, LABEL_BG_SOLID),
        (LABEL_BG_GRADIENT, LABEL_BG_GRADIENT),
    )

    info_title = forms.CharField(
        required=False,
        widget=TextBoxWidget(
            attrs={
                "section_heading": "Title",
                "section_heading_desc": "Name your gallery as you want it to be reflected on the page",
                "input_type": "text",
                "placeholder": "Enter Title",
            }
        ),
    )

    title_color = forms.CharField(
        widget=ColorPalette(
            attrs={
                "label": "Font Color",
                "section_divider": True,
            }
        ),
        required=False,
    )

    click_action = forms.ChoiceField(
        choices=action_choices,
        initial=ACTION_LARGE_IMAGE,
        widget=CustomRadioSelect(
            attrs={
                    "section_heading": "Action",
                    "section_heading_desc": "Description (click effect)",
                    "horizontal_layout": True,
                    "section_divider": True,
                },
        ),
    )

    label_bg_style = forms.ChoiceField(
        choices=label_bg_style_choices,
        initial=LABEL_BG_SOLID,
        widget=CustomRadioSelect(
            attrs={
                    "section_heading": "Label",
                    "section_sub_heading": "Background Style",
                    "horizontal_layout": True,
                },
        ),
    )

    label_bg_color = forms.CharField(
        widget=ColorPalette(
            attrs={
                "label": "Background Color",
            }
        ),
        required=False,
    )

    label_font_color = forms.CharField(
        widget=ColorPalette(
            attrs={
                "label": "Font Color",
                "section_divider": True,
            }
        ),
        required=False,
    )

    class Meta:
        entangled_fields = {
            "glossary": [
                "info_title",
                "title_color",
                "click_action",
                "label_bg_style",
                "label_bg_color",
                "label_font_color",
            ]
        }
        untangled_fields = []


class GalleryItemInline(StackedInline):
    """
    Inline form in static info block plugin
    """
    
    model = InlineCascadeElement
    form = GalleryItemForm
    raw_id_fields = ['image_file']
    verbose_name = _("Gallery Image")
    verbose_name_plural = _("Gallery Images")
    extra = 1


class ServicesBlockPluginForm(CascadeModelForm):
    """
    Store data of Services
    """

    block_title = forms.CharField(required=False, 
        widget=TextBoxWidget(
        attrs={
            "label": "Service Block Title",
            "placeholder": "Enter Title",
        }
    ),)

    bg_color = forms.CharField(
        initial="#ffffffff", required=False,
        widget=ColorPalette(
            attrs={
                "label": "Background Color",
            },
        ),
    )

    class Meta:
        entangled_fields = {
            "glossary": [
                "block_title",
                "bg_color",
            ]
        }
        untangled_fields = []
        
class ServiceBlockItemForm(CascadeModelForm):
    """
    Store data of individual item of service block plugin
    """

    image_file = CascadeImageField()

    image_alt_text = forms.CharField(
        required=False,         
        widget=TextBoxWidget(
            attrs={
                "label": "Image Alt Text",
                "placeholder": "Enter alt text for image",
            }
        )
    )
    
    service_name = forms.CharField(
        required=False,
        widget=TextBoxWidget(
            attrs={
                "label": "Service Name",
                "placeholder": "Enter Name",
            }
        ),
    )

    service_page_url = forms.CharField(
        required=False,
        widget=LinkWidget(
            ajax_view="admin:cms_page_get_published_pagelist",
            attrs = {
                "label": "Service Page Link",
                "placeholder": "Start typing...",
            }
        ),
    )

    class Meta:
        entangled_fields = {
            "glossary": [
                "image_file",
                "service_name",
                "service_page_url",
                "image_alt_text"
            ]
        }
        untangled_fields = []
        
class ServiceItemInline(StackedInline):
    """
    Inline form in Service block plugin
    """
    
    model = InlineCascadeElement
    form = ServiceBlockItemForm
    raw_id_fields = ['image_file']
    verbose_name = _("Service")
    verbose_name_plural = _("Services")
    extra = 5

class ContactUsInfoPluginForm(CascadeModelForm):
    """
    Store data of Subscribe us plugin
    """

    # title = forms.CharField(max_length=55, required=False)

    # sub_title = forms.CharField(
    #                 max_length=255, required=False, 
    #                 initial=""
    #             )

    bg_image = CascadeImageField(required=False, label="Background image")
    
    # display_default_image = forms.BooleanField(required=False, initial=True, help_text="Display default image if side image is not available.")
    
    # display_text_left = forms.BooleanField(required=False, initial=False, help_text="Display Title and subtitle to the left it will not display side image.")
    
    side_image = CascadeImageField(required=False, label="Side image")

    url=forms.CharField(required=False)

    first_location = forms.ChoiceField(
        label="Location",
        help_text="Select a locations to display first contact us detail.",
        widget=forms.Select(),
        required=False,
    )
    
    button_internallink = forms.ModelChoiceField(
        blank=True,
        required=False,
        queryset=Page.objects.filter(publisher_is_draft=False),
    )
    class Meta:
        model = SubscribePluginModel
        entangled_fields = {
            "glossary": [
                # "title",
                # "sub_title",
                "bg_image",
                # "display_default_image",
                # "display_text_left",
                "side_image",
                "button_internallink",
                "url",
                "first_location"
            ]
        }
        untangled_fields = []
    
    def __init__(self, *args, **kwargs):
        super(ContactUsInfoPluginForm, self).__init__(*args, **kwargs)
        self.client = PWAPI()
        
        # Fetch pet locations from pos
        locations_list = [
            (location["id"], location["entity"]["name"])
            for location in get_stores_data(client=self.client)
        ]
        locations_list.insert(0, ("", "Default"))

        self.fields["first_location"].choices = locations_list


class ContactUsPluginForm(CascadeModelForm):
    """
    Store data of Contact Us Plugin
    """    
    
    location_filter = forms.MultipleChoiceField(
        label="Location",
        widget=CustomCheckBox(
            attrs={
                "section_heading": "Store Locations",
                "section_sub_heading": "Select a locations by which will be displayed in contact us forms.",
                "section_divider": True,
            }
        ),
        required=False,
    )

    breeder_is = forms.ChoiceField(
        choices=ISBUTTON_CHOICES,
        initial="False",
        required=True,
        widget=CustomRadioSelect(
            attrs={
                "section_heading": "Show breeder field?",
                "section_divider": True,
            }
        ),
    )

    is_contactus_menu = forms.ChoiceField(
            choices=ISBUTTON_CHOICES,
            initial="False",
            required=True,
            widget=CustomRadioSelect(
                attrs={
                    "section_heading": "Show Contact Us floating menu",
                    "section_divider": True,
                }
            ),
        )
    class Meta:
        entangled_fields = {
            "glossary": [
                "location_filter",
                "breeder_is",
                "is_contactus_menu"
            ]
        }
        untangled_fields = []
    
    def __init__(self, *args, **kwargs):
        super(ContactUsPluginForm, self).__init__(*args, **kwargs)
        self.client = PWAPI()

        # Fetch pet locations from pos
        locations_list = [
            (location["id"], location["name"])
            for location in get_locations_list(client=self.client)
        ]
        self.fields["location_filter"].choices = locations_list

class FAQBlockTabForm(CascadeModelForm):
    """
    Store data of individual tab of faq block plugin
    """
    faq_tab_title = forms.CharField(required=False)

    class Meta:

        entangled_fields = {
            "glossary": [
                "faq_tab_title",
            ]
        }
        untangled_fields = []

class FAQTabInline(TabularInline):
    """
    Inline form in faq block plugin
    """
    
    model = InlineCascadeElement
    form = FAQBlockTabForm
    raw_id_fields = ['image_file']
    verbose_name = _("FAQ Tab")
    verbose_name_plural = _("FAQ Tabs")
    extra = 1

class FAQBlockPluginForm(CascadeModelForm):
    """
    Store data of faq block
    """

    faq_block_title = forms.CharField(required=False)

    class Meta:
        entangled_fields = {
            "glossary": [
                "faq_block_title",
            ]
        }
        untangled_fields = []

class FAQAccordionItemForm(CascadeModelForm):
    """
    Store data of individual item of faq accordion plugin
    """

    item_question = forms.CharField(required=False)
    item_answer = forms.CharField(required=False)

    class Meta:
        entangled_fields = {
            "glossary": [
                "item_question",
                "item_answer"
            ]
        }
        untangled_fields = []


class FAQItemInline(TabularInline):
    """
    Inline form in faq accordion plugin
    """
    
    model = InlineCascadeElement
    form = FAQAccordionItemForm
    raw_id_fields = ['image_file']
    verbose_name = _("FAQ Item")
    verbose_name_plural = _("FAQ Items")
    extra = 1


class FAQAccordionPluginForm(CascadeModelForm):
    """
    Store data of faq accordion
    """
    faq_acc_tab_title = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Retrieve faq_tab_title choices from parent form
        try: 
            parent_id = kwargs.get('initial',{}).get('plugin_parent') or kwargs.get('instance').parent_id
            parents_tab = InlineCascadeElement.objects.filter(cascade_element_id=parent_id)
            tab_list = [(tab.glossary['faq_tab_title'], tab.glossary['faq_tab_title']) for tab in parents_tab ]
        except Exception:
            tab_list = []
            tab_list.insert(0, (self.data['faq_acc_tab_title'], self.data['faq_acc_tab_title']))
        
        self.fields['faq_acc_tab_title'].choices = tab_list

    class Meta:
        entangled_fields = {
            "glossary": [
                "faq_acc_tab_title",
            ]
        }
        untangled_fields = []

class LocationBasePluginForm(CascadeModelForm):

    location = forms.ChoiceField(
        label="Location",
        widget=CustomRadioSelect(
            attrs={
                "section_heading": "Store Locations",
                "section_sub_heading": "Select a location, which detail will be displayed.",
                "section_divider": True,
            }
        ),
        required=False,
    )

    text_color = forms.CharField(
        widget=ColorPalette(
            attrs={
                "label": "Font Color",
            },
        ),
        required=True,
    )

    class Meta:
        entangled_fields = {
            "glossary": [
                "text_color",
                "location",
            ]
        }
        untangled_fields = []

    def __init__(self, *args, **kwargs):
        super(LocationBasePluginForm, self).__init__(*args, **kwargs)
        self.client = PWAPI()
        
        # Fetch pet locations from pos
        locations_list = [
            (location["id"], location["entity"]["name"])
            for location in get_stores_data(client=self.client)
        ]

        self.fields["location"].choices = locations_list

class LocationContactNumberPluginForm(LocationBasePluginForm):
    pass

class LocationSocialPluginForm(LocationBasePluginForm):
    pass

class ShowHidePluginForm(CascadeModelForm):

    FILTER_CHOICES = [
        (True, 'Show by Default, Hide Based on Filter Criteria'),
        (False, 'Show by Default, Hide Based on Filter Criteria')
    ]

    LOCATION_CHOICE = [
        (True, 'Location Selection')
    ]

    DATE_CHOICE = [
        (True, 'Date Range')
    ]

    sh_filter_type = forms.ChoiceField(
        choices=FILTER_CHOICES,
        initial="True",
        widget=CustomRadioSelect(),
        required=False,
    )

    sh_location_choice = forms.MultipleChoiceField(
        choices=LOCATION_CHOICE,
        widget=CustomCheckBox(),
        required=False,
    )

    sh_date_choice = forms.MultipleChoiceField(
        choices=DATE_CHOICE,
        widget=CustomCheckBox(),
        required=False,
    )

    sh_store_locations = forms.MultipleChoiceField(
        choices=[],
        widget=CustomCheckBox(),
        required=False,
    )

    sh_date_range = DateRangeField(widget = forms.HiddenInput, max_length=21, required=False)

    sh_date_selector  = DateRangeField(max_length=21, required=False)
    class Meta:
        entangled_fields = {
            "glossary": [
                "sh_filter_type",
                "sh_store_locations",
                "sh_location_choice",
                "sh_date_choice",
                "sh_date_range",
                "sh_date_selector",
            ]
        }

    def __init__(self, *args, **kwargs):
        super(ShowHidePluginForm, self).__init__(*args, **kwargs)
        client = PWAPI()
        store_data = get_stores_data(client=client)
        store_loc_choices = [(store['id'], _(store['receipt_name'])) for store in store_data]
        self.fields['sh_store_locations'].choices = store_loc_choices