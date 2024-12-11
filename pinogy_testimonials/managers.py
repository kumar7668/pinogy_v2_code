# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from parler.managers import TranslatableManager, TranslatableQuerySet


class TestimonialQuerySet(TranslatableQuerySet):
    def published(self):
        """Returns only published Testimonials."""
        return self.filter(is_published=True)

    def featured(self):
        """Returns only featured, published testimonials."""
        return self.published().filter(is_featured=True)


class TestimonialManager(TranslatableManager):
    def get_queryset(self):
        qs = TestimonialQuerySet(self.model, using=self.db)
        return qs.select_related('photo')

    # For older Djangos
    get_query_set = get_queryset

    def published(self):
        return self.get_query_set().published()

    def featured(self):
        return self.get_query_set().featured()
