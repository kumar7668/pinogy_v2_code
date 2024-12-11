from cms.models import Page
from cmsplugin_cascade.forms import CascadeModelForm
from django import forms
from django.utils.translation import gettext_lazy as _
from custom_design.widget import ColorPalette
from carousel_plugins import utils
from carousel_plugins.models import CarouselPluginModel, GridPluginModel
from pos_api.pos_client import PWAPI
from custom_design.widget import TextBoxWidget, ColorPalette, LinkWidget, CustomCheckBox, CustomRadioSelect, CKEditorTextboxWidget
from pinogy_breeds.pos_api import BreedList
from pinogy_shop.pos_api.customer import EntityClient
class CarouselPluginForm(CascadeModelForm):

    CAROUSEL_TYPE_CHOICES = [
        ("PETS", _("Pets")),
        # ("PRODUCTS", _("Products")),
        ("PROMOTIONS", _("Promotions")),
        ("TESTIMONIALS", _("Testimonials")),
        ("BRANDS",_("Brands")),
        ("BLOG", _("Blog")),
    ]

    PROMOTIONS_CHOICES = [
        ('store_promotions', _("Store Promotion")),
        ('PETZ', _("PETZ")),
        ('Astro Frequent Buyer', _("Astro Frequent Buyer")),
        ('Astro Offer', _("Astro Offer"))
    ]

    PET_LAYOUT_CHOICES = [
        (
            "carousel/includes/pet/pet_carousel_layout1.html",
            _("Pet information is displayed overlaying the image"),
        ),
        ("carousel/includes/pet/pet_carousel_layout2.html", _("No pet information")),
        (
            "carousel/includes/pet/pet_carousel_layout3.html",
            _("Pet information is displayed overlaping the image"),
        ),
        (
            "carousel/includes/pet/pet_carousel_layout4.html",
            _("Pet information is displayed below the image"),
        ),
        (
            "carousel/includes/pet/grid_layout.html",
            _("Pet Grid View With Price And Name"),
        ),
    ]
    
    PET_SOURCE_CHOICES = [
        ("DEFAULT",_("Default")),
        ("SIMILAR_PETS",_("Similar Pets (Based on breed)")),
        ("AVAILABLE_PETS",_("Available Pets (Based on breed)")),
    ]

    INFODISPLAY_CHOICES = [
        ("NAME", _("Name")),
        ("SEX", _("Sex")),
        ("BREED", _("Breed")),
        ("LOCATION", _("Location")),
    ]

    TAGDISPLAY_CHOICES = [
        ("AVAILABLE_NOW", _("Available now")),
        ("COMING_SOON", _("Coming soon")),
        ("FOUND_HOME", _("Found home")),
        ("ON_SALE", _("On sale")),
    ]

    TESTIMONIAL_LAYOUT_CHOICES = [
        ("carousel/includes/testimonial/tc_horizontal.html", _("Horizontal")),
        ("carousel/includes/testimonial/tc_vertical.html", _("Vertical")),
    ]

    BLOGL_LAYOUT_CHOICES = [
        ("carousel/includes/blog/blog_layout.html", _("Vertical")),
        ("carousel/includes/blog/blog_info_layout.html", _("Horizontal")),
    ]

    TESTIMONIAL_INFODISPLAY_CHOICES = [
        ("TITLE", _("Title")),
        ("MESSAGE", _("Message")),
        ("AUTHOR", _("Author")),
    ]

    PROMOTION_LAYOUT_CHOICES = [
        ("carousel/includes/promotion/promotion_horizontal.html", _("Horizontal")),
        ("carousel/includes/promotion/promotion_vertical.html", _("Vertical")),
    ]

    BRAND_LAYOUT_CHOICES = [
        ("carousel/includes/brand/brand_vertical_layout.html", _("Vertical")),
    ]

    BRAND_INFODISPLAY_CHOICES = [
        ("SHOW", _("Show")),
        ("DON’T SHOW", _("Don’t show")),
    ]

    PRODUCT_FILTER_CHOICES = [
        ("FEATURED", _("Featured Products")),
        ("POPULAR", _("Popular Products")),
        ("NEWEST", _("Newest Products")),
    ]

    PRODUCT_INFODISPLAY_CHOICES = [
        ("NAME", _("Name")),
        ("PRICE", _("Price")),
        ("BUTTON", _("Button ‘Add To Cart’")),
    ]

    CARDSIZE_CHOICES = [
        ("SMALL", _("Small ")),
        ("LARGE", _("Large")),
    ]

    BUTTON_STYLE = [
        ("fill", _("Fill")),
        ("outline", _("Outline")),
    ]

    carousel_type = forms.ChoiceField(
        choices=CAROUSEL_TYPE_CHOICES,
        label="Type",
        initial="PETS",
        help_text="Specify the item of carousel.",
        widget=forms.RadioSelect(),
    )

    promotions_type = forms.MultipleChoiceField(
        choices=PROMOTIONS_CHOICES,
        label="Promotions Type",
        help_text="",
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    marketing_list= forms.ChoiceField(
        choices=[],
        label="Marketing list",
        help_text="",
        widget=forms.RadioSelect(),
        required=False,
    )

    pet_layout = forms.ChoiceField(
        choices=PET_LAYOUT_CHOICES,
        label="Pet carousel's Layout",
        initial="carousel/includes/pet/pet_carousel_layout1.html",
        help_text="Specify the layout of pet carousel.",
        widget=forms.RadioSelect(),
    )

    brand_layout = forms.ChoiceField(
        choices=BRAND_LAYOUT_CHOICES,
        label="Brand carousel's Layout",
        initial="carousel/includes/brand/brand_vertical_layout.html",
        help_text="Specify the layout of brand carousel.",
        widget=forms.RadioSelect(),
        required = False
    )

    # brand_display = forms.ChoiceField(
    #     choices= BRAND_INFODISPLAY_CHOICES,
    #     label="Brand title display",
    #     initial="SHOW",
    #     help_text="Specify show or dont show brand title",
    #     widget=forms.RadioSelect(),
    # )

    pet_type = forms.MultipleChoiceField(
        label="Pet Type",
        help_text="Select pets you want to be displayed.",
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    
    pet_source = forms.ChoiceField(
        required=False,
        choices=PET_SOURCE_CHOICES,
        label="Pet Source",
        initial="DEFAULT",
        help_text="Specify the data source for pets. (Available/Similar pets use in pet/breed detail.)",
        widget=forms.RadioSelect(),
    )

    pet_status_filter = forms.MultipleChoiceField(
        label="Status",
        help_text="Select a statuses by which pets will be displayed.",
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    pet_location_filter = forms.MultipleChoiceField(
        label="Location",
        help_text="Select a locations by which pets will be displayed.",
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    pet_info_display = forms.MultipleChoiceField(
        choices=INFODISPLAY_CHOICES,
        label="Info",
        help_text="Select the information to be displayed.",
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    pet_tag_display = forms.MultipleChoiceField(
        choices=TAGDISPLAY_CHOICES,
        label="Tag",
        help_text="Select the tag to be displayed.",
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    testimonial_layout = forms.ChoiceField(
        choices=TESTIMONIAL_LAYOUT_CHOICES,
        label="Testimonial carousel's Layout",
        initial="carousel/includes/testimonial/tc_horizontal.html",
        help_text="Specify the layout of testimonial carousel.",
        widget=forms.RadioSelect(),
    )

    testimonial_info_display = forms.MultipleChoiceField(
        choices=TESTIMONIAL_INFODISPLAY_CHOICES,
        label="Info",
        help_text="Select the information to be displayed.",
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    promotion_layout = forms.ChoiceField(
        choices=PROMOTION_LAYOUT_CHOICES,
        label="Promotion carousel's Layout",
        initial="carousel/includes/promotion/promotion_horizontal.html",
        help_text="Specify the layout of promotion carousel.",
        widget=forms.RadioSelect(),
    )

    blog_layout = forms.ChoiceField(
        choices=BLOGL_LAYOUT_CHOICES,
        label="Blog carousel's Layout",
        initial="carousel/includes/blog/blog_layout.html",
        help_text="Specify the layout of blog carousel.",
        widget=forms.RadioSelect(),
        required=False
    )

    product_filter = forms.MultipleChoiceField(
        choices=PRODUCT_FILTER_CHOICES,
        label="Product filter",
        help_text="Select a filter by which products will be displayed.",
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    product_info_display = forms.MultipleChoiceField(
        choices=PRODUCT_INFODISPLAY_CHOICES,
        label="Info",
        help_text="Select the information to be displayed.",
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    card_size = forms.ChoiceField(
        choices=CARDSIZE_CHOICES,
        label="Card Size",
        initial="SMALL",
        help_text="Specify the card size of pet carousel.",
        widget=forms.RadioSelect(),
    )

    card_text_color = forms.CharField(
        widget=ColorPalette(
            attrs={
                "label": "Card text",
            },
        ),
        initial="#003f5aff",
        required = False
    )

    card_bg_color = forms.CharField(
        widget=ColorPalette(
            attrs={
                "label": "Card background",
            },
        ),
        initial="#ffffffff",
        required = False
    )

    blog_bg_color = forms.CharField(
        widget=ColorPalette(
            attrs={
                "label": "Font Color",
            },
        ), initial="#ffffffff", required=False
    )
    carous_title_color = forms.CharField(
        widget=ColorPalette(
            attrs={
                "label": "Font Color",
            },
        ), initial="#000000ff", required=False
    )

    title_text = forms.CharField(required=False)

    sub_title_text = forms.CharField(required=False)

    sub_title_text_color = forms.CharField(
        widget=ColorPalette(
            attrs={
                "label": "Font Color",
            },
        ),  initial="#000000ff", required=False
    )

    first_button_text = forms.CharField(required=False)

    first_button_link = forms.URLField(required=False)

    first_button_internallink = forms.ModelChoiceField(
        blank=True,
        required=False,
        queryset=Page.objects.filter(publisher_is_draft=False),
    )

    first_button_style = forms.ChoiceField(
        choices=BUTTON_STYLE, initial="fill", required=False
    )

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

    class Meta:
        model = CarouselPluginModel
        entangled_fields = {
            "glossary": [
                "carousel_type",
                "pet_layout",
                "pet_type",
                "pet_source",
                "pet_status_filter",
                "pet_location_filter",
                "pet_info_display",
                "pet_tag_display",
                "testimonial_layout",
                "testimonial_info_display",
                "promotion_layout",
                "blog_layout",
                "brand_layout",                
                "product_filter",
                "product_info_display",
                "card_size",
                "card_text_color",
                "card_bg_color",
                "title_text",
                "first_button_text",
                "first_button_link",
                "first_button_internallink",
                "first_button_style",
                "second_button_text",
                "second_button_link",
                "second_button_internallink",
                "second_button_style",
                "sub_title_text",
                "sub_title_text_color",
                "blog_bg_color",
                "carous_title_color",
                "promotions_type",
                "marketing_list",

            ]
        }
        untangled_fields = []

    def __init__(self, *args, **kwargs):
        super(CarouselPluginForm, self).__init__(*args, **kwargs)
        self.client = PWAPI()

        # Fetch pet types from POS
        pet_type_uniqe_list = [
            (
                pet_type.get("name", ""),
                pet_type.get("name", ""),
            )
            for pet_type in utils.get_pet_type_list(client=self.client)
            if pet_type["is_enabled"] and pet_type["available_pets_count"] > 0
        ]
        self.fields["pet_type"].choices = pet_type_uniqe_list

        # Fetch pet statues from POS
        pet_status_list = [
            (pet_status["id"], pet_status["name"])
            for pet_status in utils.get_pet_status_list(client=self.client)
            if pet_status["available_publicly"] is True
        ]
        self.fields["pet_status_filter"].choices = pet_status_list

        # Fetch pet locations from pos
        locations_list = [
            (location["id"], location["name"])
            for location in utils.get_locations_list(client=self.client)
        ]

        self.fields["pet_location_filter"].choices = locations_list

        # marketing list from api 
        client = EntityClient()
        marketingList = client.get_marketing_lists()
        marketingList = [(data['id'],data['name']) for data in marketingList.get('objects', {})]
        self.fields['marketing_list'].choices = marketingList


class GridPluginForm(CascadeModelForm):

    GRID_TYPE_CHOICES = [
        ("PETS", _("Pets")),
        ("BRANDS",_("Brands")),
        # ("PRODUCTS", _("Products")),
        ("PROMOTIONS", _("Promotions")),
        ("TESTIMONIALS", _("Testimonials")),
        # ("BLOG", _("Blog")),
    ]

    PROMOTIONS_CHOICES = [
        ('store_promotions', _("Store Promotion")),
        ('PETZ', _("PETZ")),
        ('Astro Frequent Buyer', _("Astro Frequent Buyer")),
        ('Astro Offer', _("Astro Offer"))
    ]

    PET_LAYOUT_CHOICES = [
        (
            "pet_layout_1",
            _("Pet information is displayed overlaying the image"),
        ),
        ("pet_layout_2", _("No pet information")),
        (
            "pet_layout_3",
            _("Pet information is displayed overlaping the image"),
        ),
        (
            "pet_layout_4",
            _("Pet information is displayed below the image"),
        ),
        (
            "pet_layout_5",
            _("Pet Grid View With Price And Name"),
        ),
    ]

    BRAND_LAYOUT_CHOICES = [
        (
            "brand_layout_1",
            _("Brand logo with brand name"),
        ),
        ("brand_layout_2", 
            _("Brand logo without brand name")),
    
    ]

    PROMOTIONS_LAYOUT_CHOICES = [
        (
            "promotion_layout_1",
            _("Image with text at the bottom"),
        ),
        ("promotion_layout_2", 
            _("Image left and text on the right")),
    
    ]
    TESTIMONIALS_LAYOUT_CHOICES = [
        (
            "testimonials_layout_1",
            _("Image left and text on the right"),
        ),
        ("testimonials_layout_2", 
            _("Image on the top and text at the bottom")),
    
    ]

    TESTIMONIAL_INFODISPLAY_CHOICES = [
        ("TITLE", _("Title")),
        ("MESSAGE", _("Message")),
        ("AUTHOR", _("Author")),
    ]

    FILTERS = [
        ('Pet_Type', 'Pet Type'), 
        ('Breed', 'Breed'), 
        ('Sex', 'Sex'), 
        ('Status', 'Status'), 
        ('on_sale', 'Is Pet On Sale?'), 
        ('promotion_type', 'Promotion type'),
        ]

    GRID_NUMBER_OF_ROWS = [
        (1, ('1')),
        (2, ('2')),
        (3, ('3')),
        (4, ('4')),
        (5, ('5')),
        (0, ('Unlimited grid')),
    ]
    
    GRID_CARD_SIZE = [
        ('SMALL', _('Small')),
        ('LARGE', _('Large'))
    ]

    GRID_NOTIFICATION = [
        (True, _('Show')),
        (False, _('Don’t show'))
    ]

    GRID_CARD_DETAILS = [
        ("name", _("Name")),
        ("price", _("Price")),
        ("sex", _("Sex")),
        ("breed", _("Breed")),
        ("location", _("Location")),
    ]

    BUTTON_STYLE = [
        ("fill", _("Fill")),
        ("outline", _("Outline")),
    ]

    IS_ON_SALE = [
        ("false", _("Show All")),
        ("true", _("Show on Sale")),
    ]

    PET_SEX = [
        ("male", _("Male")),
        ("female", _("Female")),
    ]

    grid_type = forms.ChoiceField(
        choices=GRID_TYPE_CHOICES,
        initial="PETS",
        widget=CustomRadioSelect(),
    )

    grid_no_of_rows = forms.ChoiceField(
        choices=GRID_NUMBER_OF_ROWS,
        initial=1,
        widget=CustomRadioSelect(
            attrs={
                'section_heading' : 'Number of rows',
                'horizontal_layout' : True,
            }
        ),
    )

    grid_card_size = forms.ChoiceField(
        choices=GRID_CARD_SIZE,
        initial='SMALL',
        widget=CustomRadioSelect(),
    )

    grid_notification = forms.ChoiceField(
        choices=GRID_NOTIFICATION,
        initial=False,
        widget=CustomRadioSelect(
            attrs={
                'horizontal_layout' : True,
            }
        ),
    )

    grid_card_details = forms.MultipleChoiceField(
        choices=GRID_CARD_DETAILS,
        required= False,
        widget=CustomCheckBox(

        ),
    )

    grid_breeds = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(),
    )

    grid_breeds_list = forms.CharField(required=False)

    pet_layout = forms.ChoiceField(
        choices=PET_LAYOUT_CHOICES,
        label="Pet carousel's Layout",
        initial="pet_layout_1",
        help_text="Specify the layout of pet carousel.",
        widget=forms.RadioSelect(),
    )
    brand_layout = forms.ChoiceField(
        choices=BRAND_LAYOUT_CHOICES,
        label="Pet carousel's Layout",
        initial="brand_layout_1",
        help_text="Specify the layout of pet carousel.",
        widget=forms.RadioSelect(),
    )
    promotion_layout = forms.ChoiceField(
        choices=PROMOTIONS_LAYOUT_CHOICES,
        label="Pet carousel's Layout",
        initial="promotion_layout_1",
        help_text="Specify the layout of pet carousel.",
        widget=forms.RadioSelect(),
    )
    testimonial_layout = forms.ChoiceField(
        choices=TESTIMONIALS_LAYOUT_CHOICES,
        label="Pet carousel's Layout",
        initial="testimonials_layout_1",
        help_text="Specify the layout of pet carousel.",
        widget=forms.RadioSelect(),
    )
    testimonial_info_display = forms.MultipleChoiceField(
        choices=TESTIMONIAL_INFODISPLAY_CHOICES,
        widget=CustomCheckBox(
        ),
        required=False,
    )

    promotion_type = forms.ChoiceField(
        choices=PROMOTIONS_CHOICES,
        help_text="Specify the layout of pet carousel.",
        widget=CustomRadioSelect(),
        required=False,
    )

    # to add the grid names
    gridName = forms.CharField(
        max_length=100, 
        required= False,
        widget=forms.TextInput(attrs = {'placeholder' : 'Name your grid as you want it to be reflected in the page structure'})
        )
    
    grid_pet_status = forms.MultipleChoiceField(
        widget=CustomCheckBox(
            attrs={
                "section_sub_heading": "Select one or more statuses.",
            }
        ),
        required=False,
    )

    grid_pet_type = forms.MultipleChoiceField(
        choices=[],
        widget=CustomCheckBox(
            attrs={
                "section_sub_heading": "Select the type of pets you want to be included.",
            }
        ),
        required=False,
    )

    pet_filter = forms.MultipleChoiceField(
        choices=FILTERS,
        widget=forms.SelectMultiple(),
        required=False,
    )

    grid_pet_location = forms.MultipleChoiceField(
        widget=CustomCheckBox(
            attrs={
                "section_sub_heading": "Limit pets to the selected locations",
            }
        ),
        required=False,
    )

    grid_Is_pet_on_sale = forms.ChoiceField(
        choices=IS_ON_SALE,
        initial='false',
        required=False,
        widget=CustomRadioSelect(
        ),
    )

    grid_pet_sex = forms.ChoiceField(
        choices=PET_SEX,
        initial='male',
        required=False,
        widget=CustomRadioSelect(

        ),
    )

    button_internallink_1 = forms.ModelChoiceField(
        blank=True,
        required=False,
        queryset=Page.objects.filter(publisher_is_draft=False),
    )

    card_text_color = forms.CharField(
        widget=ColorPalette(
            attrs={
                "label": "Card text",
            },
        ),
        initial="#003f5aff",
        required = False
    )

    card_bg_color = forms.CharField(
        widget=ColorPalette(
            attrs={
                "label": "Card background",
            },
        ),
        initial="#ffffffff",
        required = False
    )

    blog_bg_color = forms.CharField(
        widget=ColorPalette(
            attrs={
                "label": "Font Color",
            },
        ), initial="#ffffffff", required=False
    )

    title_text_color = forms.CharField(
       widget=ColorPalette(
            attrs={
                "label": "Title Color",
            },
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

    grid_button_data = forms.CharField(required=False)
    class Meta:
        model = GridPluginModel
        entangled_fields = {
            "glossary": [
                'gridName',
                "grid_type",
                "grid_card_size",
                "grid_notification",
                "pet_layout",
                'grid_card_details',
                "grid_pet_status",
                "grid_pet_type",
                "grid_pet_location",
                "grid_breeds",
                "grid_Is_pet_on_sale",
                'button_internallink_1',
                "pet_filter",
                "brand_layout",
                "grid_pet_sex",
                "grid_no_of_rows",
                'promotion_layout',
                "testimonial_layout",
                "testimonial_info_display",
                "promotion_type",

                "card_text_color",
                "card_bg_color",
                "title_text",
                "title_text_color",
                
                "sub_title_text",
                "sub_title_text_color",
                "blog_bg_color",
            ]
        }
        untangled_fields = ['grid_breeds_list', 'grid_button_data']

    def __init__(self, *args, **kwargs):
        super(GridPluginForm, self).__init__(*args, **kwargs)
        self.client = PWAPI()

        #Fetch pet types from POS
        pet_type_uniqe_list = [
            (
                pet_type.get("name", ""),
                pet_type.get("name", ""),
            )
            for pet_type in utils.get_pet_type_list(client=self.client)
            if pet_type["is_enabled"] and pet_type["available_pets_count"] > 0
        ]
        self.fields["grid_pet_type"].choices = pet_type_uniqe_list

        # Fetch pet statues from POS
        pet_status_list = [
            (pet_status["id"], pet_status["name"])
            for pet_status in utils.get_pet_status_list(client=self.client)
            if pet_status["available_publicly"] is True
        ]
        self.fields['grid_pet_status'].choices = pet_status_list

        # Fetch pet locations from pos
        locations_list = [
            (location["id"], location["name"])
            for location in utils.get_locations_list(client=self.client)
        ]
        self.fields['grid_pet_location'].choices = locations_list

        # breeds dropdown data 
        breed_obj = BreedList()
        pet_type_slug = None
        breeds_pet_type = None
        breed_list = breed_obj.get_breed_list(pet_type_slug, breeds_pet_type)
        breed_list = [ (data.name, data.name) for data in breed_list]
        self.fields['grid_breeds'].choices = breed_list