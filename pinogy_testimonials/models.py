# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.validators import MaxValueValidator
from django.urls import reverse
from django.db import models
# from django.utils.encoding import python_2_unicode_compatible
from six import python_2_unicode_compatible
from django.utils.translation import (
    ugettext_lazy as _,
    get_language,
    get_language_from_request,
    override
)

from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField
from parler.models import TranslatableModel, TranslatedFields

from .managers import TestimonialManager


@python_2_unicode_compatible
class Testimonial(TranslatableModel):
    taints_cache = True

    translations = TranslatedFields(
        subject=models.CharField(_('headline'),
            blank=False, default='', max_length=255,
            help_text=_('Enter a short headline for your story.')),
        body=models.TextField(_('your story'),
            blank=False, default='',
            help_text=_('Enter your story here.')),
        display_name=models.CharField(_('display name'),
            blank=False, default='', max_length=255,
            help_text=_('Enter the name that you would like this story to be '
                'attributed to. (E.g., “The Smith family” or “J. Doe”)')),
    )

    photo = FilerImageField(blank=True, null=True, default=None,
        verbose_name=_('your pet photo'),
        help_text=_('Share a photo of your pet. (JPG, PNG accepted up to 2MBs)'), on_delete=models.CASCADE)

    # --- private fields ---

    is_published = models.BooleanField(_('published?'), default=False,
        help_text=_('Check this box to publish this testimonial on the site.'))

    is_featured = models.BooleanField(_('featured?'), default=False,
        help_text=_('Check this box to feature this testimonial on the site.'))

    creation_date = models.DateTimeField(auto_now_add=True)

    objects = TestimonialManager()

    class Meta:
        verbose_name = _('testimonial')
        verbose_name_plural = _('testimonials')
        ordering = ('-creation_date', )

    def get_absolute_url(self, language=None):
        if language is None:
            language = get_language()
        with override(language):
            return reverse('pinogy_testimonials:testimonial', args=[self.pk, ])

    def __str__(self):
        return "Testimonial: {0}".format(self.pk)


class TestimonialPluginBase(CMSPlugin):
    # avoid reverse relation name clashes by not adding a related_name
    # from the parent Plugin model.
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin, related_name='+', parent_link=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def get_edit_mode(self, request):
        """
        Returns True only if an operator is logged-into the CMS and is in
        edit mode.
        """
        return (request.toolbar and request.toolbar.edit_mode)


class TestimonialListPluginBase(TestimonialPluginBase):
    max_testimonials = models.PositiveIntegerField(_('max. testimonials'),
        blank=False, default=5, validators=[MaxValueValidator(100), ],
        help_text=_('How many should be shown (up to 100)?'))

    restrict_to_featured = models.BooleanField(default=False,
        help_text=_('Check to show only featured testimonials.'))

    restrict_to_language = models.BooleanField(default=False,
        help_text=_('Check to only show testimonials in viewer’s langauge.'))

    IMAGE_CHOICES = (
        (0, _("show testimonials with or without images"), ),
        (1, _("only show testimonials with images"), ),
        (2, _("only show testimonials without images"), ),
    )

    image_restriction = models.PositiveSmallIntegerField(default=0,
        choices=IMAGE_CHOICES,
        help_text=_('Should there be any restriction for images?.'))

    show_add_option = models.BooleanField(default=True,
        help_text=_('Check to show option to add a new testimonial.'))

    share_button_text = models.CharField(default="Share your own pet story!",
        help_text=_('Provide your own share button text'), max_length=255)

    class Meta:
        abstract = True

    def get_testimonials(self, request):
        testimonials = Testimonial.objects

        if request and self.restrict_to_language:
            code = get_language_from_request(request, check_path=True)
            if code:
                testimonials = testimonials.translated(language_code=code)

        if self.restrict_to_featured:
            testimonials = testimonials.featured()
        else:
            testimonials = testimonials.published()

        if self.image_restriction == 1:
            testimonials = testimonials.filter(photo__isnull=False)
        elif self.image_restriction == 2:
            testimonials = testimonials.filter(photo__isnull=True)

        return testimonials.order_by('-creation_date')[:self.max_testimonials]


class TestimonialCarouselPluginModel(TestimonialListPluginBase):

    TEMPLATE_DEFAULT = 'testimonials_new/plugins/testimonial_carousel/testimonial_carousel.html'
    TEMPLATE_IMAGES_WITH_TEXT = 'testimonials_new/plugins/testimonial_carousel/images_with_text_right.html'
    TEMPLATE_IMAGES_WITH_TEXT_CURVE_CORNER = 'testimonials_new/plugins/testimonial_carousel/image_text_right_curve_corner.html'
    TEMPLATE_CARD_DESIGN = 'testimonials_new/plugins/testimonial_carousel/testimonial_card_design.html' 

    TEMPLATECHOICES = (
        (TEMPLATE_DEFAULT, _("Default"),),
        (TEMPLATE_IMAGES_WITH_TEXT, _("Image with text in right"),),
        (TEMPLATE_IMAGES_WITH_TEXT_CURVE_CORNER, _("Image with text in right and curve corner"),),
        (TEMPLATE_CARD_DESIGN, _("Card Layout"),),
    )

    available_template = models.CharField(_('Available Template'), max_length=256, default=TEMPLATE_DEFAULT, null=True, blank=True,
                                          choices=TEMPLATECHOICES,)

    displayed_count = models.PositiveIntegerField(_('displayed count'),
        blank=False, default=3, validators=[MaxValueValidator(10), ],
        help_text=_('How many testimonials displayed on carousel?'))

    display_with_star = models.BooleanField(default=True,
        help_text=_('Display star as rate of testimonial.'))

    set_padding = models.BooleanField(default=True,
        help_text=_('Set padding for testimonial item.'))



class TestimonialFormPluginModel(TestimonialPluginBase):
    def get_testimonials(self, *args, **kwargs):
        pass


class TestimonialQuotesPluginModel(TestimonialListPluginBase):
    pass


class TestimonialListsPluginModel(CMSPlugin):
    
    TEMPLATE_CURVE_CORNER = 'testimonials_new/plugins/testimonial_list/image_with_curve_corner.html'
    TEMPLATE_IMAGE_WITH_SIDE_TEXT = "testimonials_new/plugins/testimonial_list/image_with_text_side.html"

    TEMPLATECHOICES = (
        (TEMPLATE_CURVE_CORNER, _("Curve Corner Card"),),
        (TEMPLATE_IMAGE_WITH_SIDE_TEXT, _("Image with Text at Side"),),
    )

    available_template = models.CharField(_('Available Template'), max_length=256, default=TEMPLATE_CURVE_CORNER, choices=TEMPLATECHOICES,)

    displayed_count = models.PositiveIntegerField(_('displayed count'),
        blank=False, default=0,
        help_text=_('How many testimonials displayed in List? (0 for all)'))
    

class GooglePlace(models.Model):
    """
    To save google place id for reviews plugin
    """

    place_name = models.CharField(max_length=256, help_text=_('Place name same listed on google buisness.'))
    google_place_id = models.CharField(max_length=256, help_text=_('Place ID of location as per the google buisness.'))
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.place_name


class GoogleReviews(models.Model):
    """
    Store google reviews data
    """

    place = models.ForeignKey(to=GooglePlace, on_delete=models.CASCADE, related_name="place_review", default=None)
    author_name = models.CharField(max_length=256)
    author_url = models.URLField()
    profile_photo_url = models.URLField()
    rating = models.FloatField()
    text = models.TextField(help_text=_('Store Reviews description.'))
    is_published = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
