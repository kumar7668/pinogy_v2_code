import json, os
from datetime import datetime

from cms.api import add_plugin, create_page
from cms.models import Page
from colorfield.fields import ColorField
from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.validators import FileExtensionValidator
from django.db import models
from django.template.loader import get_template
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _
from pip._internal.utils.subprocess import make_command
from solo.models import SingletonModel


class ThemeImages(models.Model):

    IMAGE_TYPE_CHOICES = [
        ("logo", _("Logo")),
        ("favicon", _("Favicon")),
        ("background", _("Background"))
    ]

    image = models.ImageField(
        null=True,
        blank=True,
        default=None,
        upload_to="themeimages",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "webp"]
            )
        ],
    )

    image_type = models.CharField(max_length=30, choices=IMAGE_TYPE_CHOICES, blank=True)

    def __str__(self):
        return f"{self.image}"


class ThemeConfiguration(SingletonModel):

    FONTCOLOR_PALETTE = [
        ("#FFFFFF", _("White")),
        ("#000000", _("Black")),
    ]

    TEXT_ALIGNMENT = [
        ('left',_('Left')),
        ('right',_('Right')),
        ('center',_('Center')),
    ]
    default_font = '"Open Sans", Arial, sans-serif'

    BUTTON_CHOICES = [
        ("rectangle", _("Rectangle")),
        ("rounded", _("Rounded corners")),
        ("pill", _("Pill")),
    ]

    BUTTON_STYLE = [
        ("fill", _("Fill")),
        ("outline", _("Outline")),
    ]

    BUTTON_COLOR_PATTERN = [
        ("F1", _("Fill primary color with white text")),
        ("F2", _("Fill secondary color with white text")),
        ("F3", _("Fill white color with primary color text")),
        ("F4", _("Fill white color with secondary color text")),
        ("O1", _("Outline and text primary color")),
        ("O2", _("Outline and text secondary color")),
        ("O3", _("Outline and text black color")),
        ("O4", _("Outline and text white color")),
    ]

    primary_color = ColorField(format="hexa", default="#003F5AFF")

    secondary_color = ColorField(format="hexa", default="#12BBD2FF")

    highlight_color = ColorField(format = 'hexa', default='#EB8207FF')

    alert_color = ColorField(format = 'hexa', default= '#A40000FF')

    selected_logo = models.ForeignKey(
        ThemeImages,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="selected_logo",
    )

    selected_favicon = models.ForeignKey(
        ThemeImages,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="selected_favicon",
    )

    selected_background = models.ForeignKey(
        ThemeImages,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="selected_background",
    )

    heading_font = models.CharField(
        max_length=100, default=default_font
    )

    general_font = models.CharField(
        max_length=100, default=default_font
    )

    button_font = models.CharField(
        max_length=100, default=default_font
    )

    primary_button_shape = models.CharField(
        max_length=100, default="rectangle", choices=BUTTON_CHOICES
    )

    image_shape = models.CharField(
        max_length=100, default="rectangle", choices=BUTTON_CHOICES
    )

    image_radius= models.CharField(
        max_length=100, default="0"
    )

    primary_button_style = models.CharField(
        max_length=100, default="fill", choices=BUTTON_STYLE
    )

    primary_button_color_pattern = models.CharField(
        max_length=100, default="F1", choices=BUTTON_COLOR_PATTERN
    )

    secondary_button_style = models.CharField(
        max_length=100, default="outline", choices=BUTTON_STYLE
    )

    secondary_button_color_pattern = models.CharField(
        max_length=100, default="O1", choices=BUTTON_COLOR_PATTERN
    )

    file_version = models.CharField(max_length=14, blank=True, null=True)

    theme_json = models.FileField(
        upload_to="themejson",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(allowed_extensions=["json"])],
        help_text=f'<br/><b>Download sample_theme.json file </b><a href="{static("json/sample_theme.json")}" download="sample_theme.json">Click here</a>',  # noqa
    )

    font_alignment = models.CharField(max_length=10,default='left', choices=TEXT_ALIGNMENT) # this column is added to save the text align like left, right or center

    def __str__(self):
        return "Theme Configuration"
    
    def delete_old_css_files(self, theme_folder_location, current_file_name):
        """
        delete the all old css files and keep only newly created file
        """
        media_location = f"{settings.MEDIA_ROOT}/{theme_folder_location}"
        try:
            # List all files in the media_location folder
            files = os.listdir(media_location)

            for file in files:
                # Check if the file is a CSS file and not the current_file_name
                if file.lower().endswith('.css') and file != current_file_name:
                    file_path = os.path.join(media_location, file)
                    os.remove(file_path)

        except Exception as e:
            print(f"An error occurred: {e}")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        file_storage = default_storage

        # generate color css base on new theme configuration
        css_template = get_template("websitetheme_template.html")
        rendered_template = css_template.render()

        # generate file version for naming new css
        self.file_version = datetime.now().strftime("%Y%m%d%H%M%S")
        media_location = "themecss/"
        css_file_name = f"websitetheme_{self.file_version}.css"

        # save to default storage for retrieval
        file_storage.save(
            f"{settings.MEDIA_ROOT}/{media_location}/{css_file_name}", ContentFile(rendered_template)
        )
        make_command("python", "manage.py", "collectstatic", "--noinput")

        self.delete_old_css_files(media_location, css_file_name)

        super().save(*args, **kwargs)

    def get_themecss_file(self):
        return f"/media/themecss/websitetheme_{self.file_version}.css"


class TemplateConfig(SingletonModel):

    TEMPLATECHOICES = (
        (
            "template1",
            _("Template1"),
        ),
        (
            "template2",
            _("Template2"),
        ),
    )

    available_template = models.CharField(
        default="template1", choices=TEMPLATECHOICES, max_length=255
    )

    template_json = models.FileField(
        upload_to="pagejson",
        blank=True,
        null=True,
        default=None,
        validators=[FileExtensionValidator(allowed_extensions=["json"])],
        help_text=f'<br/><b>Download sample_template.json file </b><a href="{static("json/sample_template.json")}" download="sample_template.json">Click here</a>',  # noqa
    )

    def __str__(self):
        return f"{self.available_template}"

    def save(self, *args, **kwargs):
        super(TemplateConfig, self).save(*args, **kwargs)

        if self.template_json:
            templatefile = self.template_json.path
        else:
            templatefile = finders.find(f"json/{self.available_template}.json")

        # Open json file
        with open(templatefile) as file:
            templates_data = json.load(file)

        for page_config in templates_data:
            # Get page status if page is already created or not
            pagecreated = Page.objects.filter(
                reverse_id=page_config.get("page_data").get("reverse_id")
            ).first()

            if not pagecreated:
                page_data = page_config.get("page_data")

                # Create page using data which is mentioned in repective template file
                page = create_page(**page_data)

                # Set page as homepage if pagedata have is_home attribute in json
                if page_config.get("is_home"):
                    _ = page.set_as_homepage()

                # Get placeholder from page currenty its is static "Content"
                placeholder = page.placeholders.get(slot="content")

                # Iterate trough plugins and add in previous placeholder
                for plugin_config in page_config.get("plugins", []):

                    # Get plugin name and data form file
                    plugin_name = plugin_config.get("plugin_name")
                    plugin_data = plugin_config.get("data")

                    # Add plugin in page
                    _ = add_plugin(placeholder, plugin_name, "en", **plugin_data)
