# -*- coding: utf-8 -*-

from __future__ import unicode_literals
try:
    from django.core.urlresolvers import reverse_lazy
except ModuleNotFoundError as e:
    from django.urls import reverse_lazy

from django.views.generic import FormView, TemplateView, DetailView, ListView

from filer.models import Image
from pos_api.pos_client import PWAPI

from common_plugins import utils
from .models import Testimonial
from .forms import TestimonialCreateForm
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.shortcuts import render
import PIL
class TestimonialCreateView(FormView):
    # content_type = Testimonial # TODO: it is necessary to check the execution of this bug on production in a robot with nginx

    form_class = TestimonialCreateForm
    http_methods = [u'get', u'post', ]
    template_name = 'testimonials_new/testimonial_create.html'
    success_url = reverse_lazy('pinogy_testimonials:testimonial_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testimonials'] = Testimonial.objects.published()
        return context

    def form_valid(self, form):
        testimonial = form.save()
        img_upload = self.get_form_kwargs().get('files').get('img_upload', False)
        client = PWAPI()

        if img_upload:
            original_filename = img_upload.name
            if hasattr(img_upload, "temporary_file_path"):
                # A TemporaryUploadedFile
                with open(img_upload.temporary_file_path()):
                    photo = Image.objects.create(
                        owner=None,
                        original_filename=original_filename, file=img_upload)
            else:
                # An InMemoryUploadedFile
                photo = Image.objects.create(
                    owner=None,
                    original_filename=original_filename, file=img_upload)
        else:
            photo = None
        testimonial.photo = photo
        testimonial.save()

        if testimonial.photo:
            x = form.cleaned_data.get('x')
            y = form.cleaned_data.get('y')
            w = form.cleaned_data.get('width')
            h = form.cleaned_data.get('height')

            image = PIL.Image.open(form.cleaned_data.get('img_upload'))
            cropped_image = image.crop((x, y, w+x, h+y))
            resized_image = cropped_image.resize((500, 500), PIL.Image.ANTIALIAS)
            resized_image.save(testimonial.photo.path)

        return super(TestimonialCreateView, self).form_valid(form)

def cropped_image(x, y, width, height, file_image):
    image = PIL.Image.open(file_image)
    cropped_image = image.crop((x, y, width+x, height+y))
    resized_image = cropped_image.resize((500, 500), PIL.Image.ANTIALIAS)
    resized_image.save(file_image.path)

class TestimonialSuccessView(TemplateView):
    model = Testimonial
    template_name = 'testimonials_new/testimonial_success.html'
    redirect_key = 'redirect'
    cache = False

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      dict(is_redirect=request.GET.get(self.redirect_key, 'true') != 'false'))


class TestimonialAllView(ListView):
    form_class = TestimonialCreateForm
    model = Testimonial
    template_name = 'testimonials_new/testimonial_all.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(TestimonialAllView, self).get_context_data(**kwargs)
        all_testimonial = Testimonial.objects.published()
        paginator = Paginator(all_testimonial, self.paginate_by)

        page = self.request.GET.get('page', 0)

        try:
            page = int(page)
        except (TypeError, ValueError):
            page = 0

        try:
            testimonials = paginator.page(page)
        except PageNotAnInteger:
            testimonials = paginator.page(1)
        except EmptyPage:
            testimonials = paginator.page(paginator.num_pages)
        if paginator.num_pages < 6:
            page_range = range(1, paginator.num_pages+1)
        else:
            if page < 4:
                page_range = range(1,6)
            else:
                if page+3 > paginator.num_pages+1:
                    page_range = range(paginator.num_pages-4, paginator.num_pages+1)
                else:
                    page_range = range(page-2, page+3)
        context['page_range'] = page_range
        context['testimonials'] = testimonials
        context['is_photo_exists'] = all_testimonial.filter(photo__isnull=True).exists()
        return context


class TestimonialDetailView(DetailView):
    model = Testimonial
    template_name = 'testimonials_new/testimonial_detail.html'
