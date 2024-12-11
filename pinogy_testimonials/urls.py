# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    TestimonialCreateView,
    TestimonialDetailView,
    TestimonialSuccessView,
    TestimonialAllView
)

urlpatterns = [
    url(r'^$', TestimonialCreateView.as_view(), name='create_testimonial'),
    url(r'^(?P<pk>\d+)/$', TestimonialDetailView.as_view(), name='testimonial_detail'),
    url(r'^.*thank-you/$', TestimonialSuccessView.as_view(), name='testimonial_success'),
    url(r'^all/$', TestimonialAllView.as_view(), name='testimonial_all')

]
