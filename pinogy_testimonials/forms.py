# -*- coding: utf-8 -*-
import io
from PIL import Image
from filer.models import Image as filer_image
from django import forms
# from django.forms import ModelForm
from django.core.files.images import ImageFile
from parler.forms import TranslatableModelForm
from django.utils.translation import ugettext_lazy as _
from cmsplugin_cascade.forms import CascadeModelForm

from .models import Testimonial

from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class TestimonialBaseForm(TranslatableModelForm):
    required_css_class = 'required'

    required_fields = []

    def __init__(self, *args, **kwargs):
        super(TestimonialBaseForm, self).__init__(*args, **kwargs)
        # We wish for some fields to be mandatory on THIS form
        for field in self.required_fields:
            self.fields[field].required = True

    def clean(self):
        cleaned_data = super(TestimonialBaseForm, self).clean()
        # Do custom validation here.
        return cleaned_data


class TestimonialCreateForm(TestimonialBaseForm):

    # We're using a FilerImageField in our model
    img_upload = forms.ImageField(label='Select an image', required=False)
    captcha = ReCaptchaField(error_messages = {'required': "Captcha is required"})
    x = forms.FloatField(widget=forms.HiddenInput(), required=False, initial=0.0)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False, initial=0.0)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False, initial=100.0)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False, initial=100.0)

    class Meta:
        model = Testimonial
        fields = [
            "subject",
            "body",
            "display_name",
            "img_upload",
            "x",
            "y",
            "width",
            "height",
        ]

        widgets = {
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control", "rows": "4"}),
            "display_name": forms.TextInput(attrs={"class": "form-control"}),
        }
        # required_fields = ["subject", "body", "display_name", "captcha" ]
        required_fields = ["subject", "body", "display_name",]

    # def save(self):
    #     photo = super(TestimonialCreateForm, self).save()

    #     x = self.cleaned_data.get('x')
    #     y = self.cleaned_data.get('y')
    #     w = self.cleaned_data.get('width')
    #     h = self.cleaned_data.get('height')

    #     print(self.cleaned_data.get("img_upload"), '--------------------')
    #     print(type(self.cleaned_data.get("img_upload")), '--------------------2')

    #     image = Image.open(self.cleaned_data.get("img_upload"))
    #     cropped_image = image.crop((x, y, w+x, h+y))
    #     resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
    #     photo.img_upload = resized_image.save(self.cleaned_data.get("img_upload"))
        
        
    #     return photo

    
class ReviewCarouselPluginForm(CascadeModelForm):
    title_for_google_reviews = forms.CharField(max_length=300, required=False, help_text=_('Enter a title for google reviews'))
    location_name = forms.CharField(max_length=55, help_text=_('Enter location name same as google maps.'))
    second_location_name = forms.CharField(max_length=55, required=False, help_text=_('Enter Second location name same as google maps.'))
    
    minimum_rating = forms.IntegerField(min_value=0, max_value=5,
        help_text=_('Enter minimum rating to show review on website.')                     
    )
    
    class Meta:
        entangled_fields = {
            "glossary": [
                "title_for_google_reviews",
                "location_name",
                "second_location_name",
                "minimum_rating"
            ]
        }
        untangled_fields = []