# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import django.urls
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _
from cmsplugin_cascade.plugin_base import CascadePluginBase

from .forms import TestimonialCreateForm, ReviewCarouselPluginForm
from .models import (
    Testimonial,
    TestimonialCarouselPluginModel,
    TestimonialFormPluginModel,
    TestimonialQuotesPluginModel,
    TestimonialListsPluginModel,
)
from .utils import get_google_reviews_list


class PinogyPluginBase(CMSPluginBase):
    module = "Pinogy"


class TestimonialCarouselPlugin(PinogyPluginBase):
    model = TestimonialCarouselPluginModel
    name = _("Testimonial Carousel")
    render_template = "testimonials_new/plugins/testimonial_carousel/testimonial_carousel.html"

    def render(self, context, instance, placeholder):
        request = context.get('request')
        context["instance"] = instance
        try:
            context["share_url"] = django.urls.reverse(
                'pinogy_testimonials:create_testimonial')
        except:
            context["share_url"] = None
        context["form"] = TestimonialCreateForm()

        cache_key = f'pinogy_testimonials:testimonial_carousel:testimonial_list-{instance.id}'
        result = cache.get(cache_key)
        if result is None:
            context["testimonial_list"] = instance.get_testimonials(request)
            cache.set(cache_key, context["testimonial_list"], settings.CACHE_MIDDLEWARE_SECONDS)
        else:
            context["testimonial_list"] = result
        # if page with TestimonialAllView does not exist NoReverseMatch will be throwed
        try:
            context["testimonial_all_view_url"] = django.urls.reverse('pinogy_testimonials:testimonial_all')
        except django.urls.NoReverseMatch as e:
            pass

        return context
    
    def get_render_template(self, context, instance, placeholder):
        if instance.available_template:
            return instance.available_template

        return "testimonials_new/plugins/testimonial_carousel/testimonial_carousel.html"

plugin_pool.register_plugin(TestimonialCarouselPlugin)


class TestimonialFormPlugin(PinogyPluginBase):
    model = TestimonialFormPluginModel
    name = _("Testimonial Form")
    render_template = "testimonials_new/plugins/testimonial_form.html"

    def render(self, context, instance, placeholder):
        request = context.get('request')
        context["instance"] = instance
        try:
            context["form_action"] = django.urls.reverse(
                'pinogy_testimonials:create_testimonial')
        except:
            context["form_action"] = None
        context["form"] = TestimonialCreateForm()
        context["testimonial_list"] = instance.get_testimonials(request)
        return context


plugin_pool.register_plugin(TestimonialFormPlugin)


class TestimonialQuotesPlugin(PinogyPluginBase):
    module = "Pinogy"
    model = TestimonialQuotesPluginModel
    name = _("Testimonial Quotes")
    render_template = "testimonials_new/plugins/testimonial_quotes.html"

    def render(self, context, instance, placeholder):
        request = context.get('request')
        context["instance"] = instance
        try:
            context["share_url"] = django.urls.reverse(
                'pinogy_testimonials:create_testimonial')
        except:
            context["share_url"] = None
        context["form"] = TestimonialCreateForm()
        context["testimonial_list"] = instance.get_testimonials(request)
        return context

plugin_pool.register_plugin(TestimonialQuotesPlugin)


class TestimonialListsPlugin(PinogyPluginBase):
    module = "Pinogy"
    model = TestimonialListsPluginModel
    name = _("Testimonial Lists")
    render_template = "testimonials_new/plugins/testimonial_list/image_with_curve_corner.html"

    def render(self, context, instance, placeholder):
        cache_key = f'pinogy_testimonials:testimonial_list_plugin-{instance.id}-{instance.displayed_count}'
        result = cache.get(cache_key)
        if result:
            context['testimonial_list'] = result
        else:
            displayed_count = None
            if instance.displayed_count:
                displayed_count = instance.displayed_count
            context['testimonial_list'] = Testimonial.objects.filter(photo__isnull=False, is_published=True).order_by('-creation_date')[0:displayed_count]
            cache.set(cache_key, context["testimonial_list"], settings.CACHE_MIDDLEWARE_SECONDS)
        return context

    def get_render_template(self, context, instance, placeholder):
        if instance.available_template:
            return instance.available_template

        return "testimonials_new/plugins/testimonial_list/image_with_curve_corner.html"

plugin_pool.register_plugin(TestimonialListsPlugin)


class ReviewCarouselPlugin(CascadePluginBase):
    module = "Review"
    form = ReviewCarouselPluginForm
    name = _("Google Review Carousel")
    render_template = "testimonials_new/plugins/review_carousel/review_carousel.html"
    
    def render(self, context, instance, placeholder):
        
        reviews_data = get_google_reviews_list(
            first_location=instance.glossary["location_name"],
            second_location=instance.glossary.get("second_location_name"),
            minimum_rating=instance.glossary["minimum_rating"]
        )
            
        context["review_list"] = reviews_data
        context["instance"] = instance
        
        return context
    
plugin_pool.register_plugin(ReviewCarouselPlugin)
