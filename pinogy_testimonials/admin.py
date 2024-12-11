# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
# from django.utils.translation import ugettext as _

from parler.admin import TranslatableAdmin
# from pinogy_common.admin import (
#     AllTranslationsMixin, MakePublished, MakeFeatured)

from .models import Testimonial, GooglePlace, GoogleReviews
from django.utils.safestring import mark_safe

from django.utils.translation import ungettext, ugettext as _

class AdminActionBase:
    def message_user(self, modeladmin, request, model, count, state):
        msg = ungettext(
            "%(count)d %(obj_name)s was set to %(state)s.",
            "%(count)d %(obj_name)s were set to %(state)s.",
            count) % {
                'count': count,
                'obj_name': model._meta.verbose_name_raw,
                'state': state}
        modeladmin.message_user(request, msg)

class MakePublished(AdminActionBase):
    def __init__(self, is_true, obj_name_plural):
        self.is_true = is_true
        self.obj_name_plural = obj_name_plural

    def __call__(self, modeladmin, request, queryset):
        model = queryset.model
        count = queryset.update(is_published=self.is_true)
        self.message_user(modeladmin, request, model, count, "published")

    @property
    def __name__(self):
        if self.is_true:
            return "make_published"
        else:
            return "make_not_published"

    @property
    def short_description(self):
        return _("Mark selected {0} as {1}").format(
            MakeFeatured.obj_name_plural,
            "not published" if MakeFeatured.is_true else "published",
        )


class MakeFeatured(AdminActionBase):
    def __init__(self, is_true, obj_name_plural):
        self.is_true = is_true
        self.obj_name_plural = obj_name_plural

    def __call__(self, modeladmin, request, queryset):
        model = queryset.model
        count = queryset.update(is_featured=self.is_true)
        self.message_user(modeladmin, request, model, count, "featured")

    @property
    def __name__(self):
        if self.is_true:
            return "make_featured"
        else:
            return "make_not_featured"

    @property
    def short_description(self):
        return _("Mark selected {0} as {1}").format(
            MakeFeatured.obj_name_plural,
            "not featured" if MakeFeatured.is_true else "featured",
        )




class TestimonialAdmin(TranslatableAdmin):
    list_display = (
        '__str__', 'subject', 'display_name', 'creation_date',
        'is_published', 'is_featured', '_preview',)
    list_editable = ('is_published', 'is_featured', )
    actions = (
        MakePublished(True, "testimonials"),
        MakePublished(False, "testimonials"),
        MakeFeatured(True, "testimonials"),
        MakeFeatured(False, "testimonials"),
    )
    readonly_fields = ('creation_date', )

    def _preview(self, obj):
        return mark_safe(obj.body)

    fieldsets = (
        (_('Publicly Visible'), {
            'fields': (
                'subject',
                'body',
                'display_name',
                'photo',
            ),
        }),
        (_('Meta'), {
            'fields': (
                ('is_published', 'is_featured', ),
                'creation_date',
            ),
        }),
    )

admin.site.register(Testimonial, TestimonialAdmin)

class GooglePlaceAdmin(admin.ModelAdmin):
    list_display = (
        'place_name', 'is_active'
    )

admin.site.register(GooglePlace, GooglePlaceAdmin)

class GoogleReviewsAdmin(admin.ModelAdmin):
    list_display = (
        'author_name', 'is_published', 'rating', 'place', 'text',  'author_url', 'profile_photo_url', 'created_at', 'updated_at',
    )
    actions = (
        MakePublished(True, "reviews"),
        MakePublished(False, "reviews"),
    )
    readonly_fields = ('created_at', )

admin.site.register(GoogleReviews, GoogleReviewsAdmin)