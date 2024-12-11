# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class TestimonialsApphook(CMSApp):
    name = "Testimonials"
    app_name = "pinogy_testimonials"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["pinogy_testimonials.urls", ]

apphook_pool.register(TestimonialsApphook)
