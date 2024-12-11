import os

from cmsplugin_cascade.models_base import CascadeModelBase
from django.core.validators import FileExtensionValidator
from django.db import models
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _
from filer.fields.image import FilerImageField
from django.core.validators import  MinValueValidator
from cms.models import Page

from custom_design.models import ThemeImages

from django.db.models import JSONField
import json

class PopupPluginModel(CMSPlugin):
    btn_text = models.CharField(max_length = 50,blank=True, null = True)

    popuptitle = models.CharField(max_length = 40,blank=True, null = True)
    
    popuptitlecolor = models.CharField(max_length = 40,blank=True, null = True)

    popupmessage = models.CharField(max_length = 40,blank=True, null = True)
    
    popupmessagecolor = models.CharField(max_length = 40,blank=True, null = True)
    
class BannerPluginModel(CascadeModelBase):

    image = models.ImageField(
        null=True,
        blank=True,
        default=None,
        upload_to="background",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "webp"]
            )
        ],
    )
    button_data = JSONField()

    mobimage = models.ImageField(
        null=True,
        blank=True,
        default=None,
        upload_to="background",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "webp"]
            )
        ],
    )

    def save(self, *args, **kwargs):
        if isinstance(self.glossary, dict):
            img_internallink = self.glossary.get('img_internallink', None)
            if img_internallink:
                page = Page.objects.get(id = img_internallink.get('pk'))
                if page:
                    img_internallink['page_link'] = page.get_absolute_url()
                else:
                    img_internallink['page_link'] = ""

        if isinstance(self.button_data, str):
            self.button_data = json.loads(self.button_data)
            for i in range(len(self.button_data)):
                internallink = self.button_data['btn'+str(i+1)]['id_button_internallink']
                self.button_data['btn'+str(i+1)]['internallink_id'] = internallink
                if internallink:
                    page = Page.objects.get(id = internallink)
                    if page:
                        self.button_data['btn'+str(i+1)]['id_button_internallink'] = page.get_absolute_url()
                        
        super(BannerPluginModel, self).save(*args, **kwargs)

class HeaderPluginModel(CascadeModelBase):

    logo = models.ForeignKey(
        ThemeImages,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="header_logo",
    )


class External_links(models.Model):
    BUTTON_TARGET_TYPE = [
        ("internal", _("Internal link"),),
        ("external", _("External link"),),
    ]
    BUTTON_TARGET_CHOICES = [
        ("_self", _("Same Window"),),
        ("_blank", _("New Window"),),
    ]
    ext_page = models.ForeignKey(Page,on_delete=models.CASCADE, related_name='external_link', blank=True,null=True)
    exernal_target = models.CharField(choices=BUTTON_TARGET_CHOICES,max_length= 28,default='_self',blank=True,null=True)
    exernal_type = models.CharField(choices=BUTTON_TARGET_TYPE,max_length= 28,default='_self',blank=True,null=True)
    internal_link_id = models.CharField(max_length=80, blank=True, null=True)
    exernal_link_name = models.CharField(max_length=30, blank=True, null=True)
    exernal_link_url = models.CharField(max_length=100, blank=True, null=True)
    parentId = models.CharField(max_length=100, null= True, blank= True)
    childId = models.CharField(max_length=100,unique=True, null= True, blank= True)
    draftId = models.CharField(max_length=100,null= True, blank= True)
    
class InstagramFeedPluginModel(CMSPlugin):
    access_token = models.CharField(max_length=255)


class InstagramData(models.Model):
    """
    Store instagram feeds data
    """
    plugin = models.ForeignKey(to=InstagramFeedPluginModel, on_delete=models.CASCADE, default=None)
    post_id = models.CharField(max_length=255)
    permalink = models.URLField()
    media_url = models.CharField(max_length=500)
    caption = models.CharField(max_length=256,null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class FooterPluginModel(CascadeModelBase):

    logo = models.ForeignKey(
        ThemeImages,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="footer_logo",
    )
    external_quick_links = JSONField(default=dict)


class InfoBlockFirstPluginModel(CascadeModelBase):

    image = models.ImageField(
        null=True,
        blank=True,
        default=None,
        upload_to="background",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "webp"]
            )
        ],
    )
    image_left = models.ImageField(
        null=True,
        blank=True,
        default=None,
        upload_to="background",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "webp"]
            )
        ],
    )
    image_right = models.ImageField(
        null=True,
        blank=True,
        default=None,
        upload_to="background",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "webp"]
            )
        ],
    )

    mobimage = models.ImageField(
        null=True,
        blank=True,
        default=None,
        upload_to="background",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "webp"]
            )
        ],
    )

    bg_image = models.ImageField(
        null=True,
        blank=True,
        default=None,
        upload_to="background",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "webp"]
            )
        ],
    )
    
    video = models.FileField(
        null=True,
        blank=True,
        default=None,
        upload_to="background",
    )

    button_data = JSONField(default=dict)
    
    def get_video_extension(self):
        _, extension = os.path.splitext(self.video.name)
        return extension.lstrip('.')

    def save(self, *args, **kwargs):
        if isinstance(self.button_data, str):
            self.button_data = json.loads(self.button_data)
            for i in range(len(self.button_data)):
                internallink = self.button_data['btn'+str(i+1)]['id_button_internallink']
                self.button_data['btn'+str(i+1)]['internallink_id'] = internallink
                if internallink:
                    page = Page.objects.get(id = internallink)
                    if page:
                        self.button_data['btn'+str(i+1)]['id_button_internallink'] = page.get_absolute_url()
                        
        super(InfoBlockFirstPluginModel, self).save(*args, **kwargs)


class InfoBlockSecondPluginModel(CascadeModelBase):

    image_left = models.ImageField(
        null=True,
        blank=True,
        default=None,
        upload_to="background",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "webp"]
            )
        ],
    )

    image_right = models.ImageField(
        null=True,
        blank=True,
        default=None,
        upload_to="background",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "webp"]
            )
        ],
    )


class SliderPluginModel(CascadeModelBase):
    pass


class SubscribePluginModel(CascadeModelBase):
     newsletter_image = models.ImageField(
        null=True,
        blank=True,
        default=None,
        upload_to="background",
        max_length=255,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "webp"]
            )
        ],
    )
     newsletter_left_image = models.ImageField(
        null=True,
        blank=True,
        default=None,
        upload_to="background",
        max_length=255,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "webp"]
            )
        ],
    )
     newsletter_right_image = models.ImageField(
        null=True,
        blank=True,
        default=None,
        upload_to="background",
        max_length=255,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "webp"]
            )
        ],
    )
     newsletter_bg_image = models.ImageField(
        null=True,
        blank=True,
        default=None,
        upload_to="background",
        max_length=255,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "webp"]
            )
        ],
    )

class UnSubscribePluginModel(CascadeModelBase):
    pass



class GalleryPluginModel(CascadeModelBase):

    image = models.ImageField(
        null=True,
        blank=True,
        default=None,
        upload_to="background",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "webp"]
            )
        ],
    )

class ContactUsInfoPluginModel(CascadeModelBase):
    pass


class CardCarouselModel(CMSPlugin):
    card_background = FilerImageField(on_delete=models.SET_NULL, null=True, blank=True, default=None)

    css_class = models.CharField(max_length=255,null=True,blank=True)

    slides_to_scroll = models.PositiveIntegerField(_("slides to scroll"),default=1,validators = [MinValueValidator(1)],
                                                    help_text=_('This variable allows you to set the  amount of '
                                                    'items to scroll at a time.'))

    items = models.PositiveSmallIntegerField(_('items'),
                                            blank=False,  default=1,
                                            help_text=_('This variable allows you to set the maximum amount of '
                                                        'items displayed at a time with the widest browser width.'))


    items_desktop = models.PositiveSmallIntegerField(_('items for desktop'),
                                                    blank=False, default=1,
                                                    help_text=_(
                                                        'The number of items to display when the client browser '
                                                        'is at "desktop" width.'))



    items_tablet = models.PositiveSmallIntegerField(_('items for tablet'),
                                                    blank=False, default=1,
                                                    help_text=_(
                                                        'The number of items to display when the client browser '
                                                        'is at "tablet" width.'))

    items_mobile = models.PositiveSmallIntegerField(_('items for mobile'),
                                                    blank=False, default=1,
                                                    help_text=_(
                                                        'The number of items to display when the client browser '
                                                        'is at "mobile" width.'))

class TabsCompoPluginModel(CMSPlugin):
    STYLE_CHOICES = [
        ('tabs', 'Tabs'),
        ('pills', 'Pills'),
    ]

    ALIGNMENT_CHOICES = [
        ('','Justify start'),
        ('nav-fill', 'Fill'),
        ('justify-content-center', 'Justify center'),
        ('justify-content-end', 'Justify end'),
        ('flex-column', 'Column'),
    ]

    ANIMATION_CHOICES = [
        ('','-----'),
        ('fade', 'Fade'),
    ]

    style = models.CharField(
        max_length=255,
        choices=STYLE_CHOICES,
        default='tabs',
        verbose_name='Type',
        blank=True 
    )

    alignment = models.CharField(
        max_length=255,
        choices=ALIGNMENT_CHOICES,
        default='',
        verbose_name='Alignment',
        blank=True 
    )

    animation = models.CharField(
        max_length=255,
        choices=ANIMATION_CHOICES,
        default='',
        verbose_name='Animation',
        blank=True 
    )




class TabItemCompoPluginModel(CMSPlugin):
    title = models.CharField(max_length=255, null=True, blank=True)