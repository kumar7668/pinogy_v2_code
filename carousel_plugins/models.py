
import binascii
import io
import os
from random import choice
from string import ascii_uppercase
from django.db import models
from cmsplugin_cascade.models_base import CascadeModelBase
from django.db import models


# Create your models here.
class CarouselPluginModel(CascadeModelBase):

    def get_short_description(self):
        plugin_display_text = ''

        if isinstance(self.glossary, dict):
            if self.glossary.get("title_text"):
                plugin_display_text = f'({self.glossary.get("title_text")})'
            elif self.glossary.get("carousel_type"):
                plugin_display_text = f'({self.glossary.get("carousel_type")})'

        return plugin_display_text
class GridPluginModel(CascadeModelBase):
    
    grid_breeds_list = models.JSONField(default=list)

    grid_button_data = models.JSONField(default=dict)
    
    def get_short_description(self):
        plugin_display_text = ''

        if isinstance(self.glossary, dict):
            if self.glossary.get("title_text"):
                plugin_display_text = f'({self.glossary.get("title_text")})'
            elif self.glossary.get("carousel_type"):
                plugin_display_text = f'({self.glossary.get("carousel_type")})'

        return plugin_display_text
class BrandImage(models.Model):

    file_content = models.FileField(upload_to='ap_media', blank=False, null=False)
    file_name = models.CharField(max_length=1000, blank=True, null=True, default=None)
    file_extension = models.CharField('file_extension', max_length=32, blank=True, null=True, default=None)

    brand_id = models.IntegerField(default=-1, blank=False, null=False)
    brand_image_id = models.IntegerField(default=-1, blank=False, null=False)

    def save_file(self, binary_file_content=None):
        random_string = ''.join(choice(ascii_uppercase) for _ in range(12))
        random_file_name = '{0}.{1}'.format(random_string, self.file_extension)

        data = binascii.a2b_base64(binary_file_content)
        stream = io.BytesIO(data)
        self.file_content.save(random_file_name, stream, save=True)
        self.file_name = random_string
        self.save()

    def delete_file(self):
        filename = self.file_content.path
        if os.path.exists(filename) and os.path.isfile(filename):
            os.remove(filename)

    @property
    def url(self):
        return self.file_content.url

    def __str__(self):
        return "Brand-{1} image-{2}".format(self.pk, self.brand_id, self.brand_image_id)

class PromotionImage(models.Model):

    file_content = models.FileField(upload_to='ap_media', blank=False, null=False)
    file_name = models.CharField(max_length=1000, blank=True, null=True, default=None)
    file_extension = models.CharField('file_extension', max_length=32, blank=True, null=True, default=None)

    promotion_id = models.IntegerField(default=-1, blank=False, null=False)
    file_id = models.IntegerField(default=-1, blank=False, null=False)

    def save_file(self, binary_file_content=None):
        random_string = ''.join(choice(ascii_uppercase) for _ in range(12))
        random_file_name = '{0}.{1}'.format(random_string, self.file_extension)

        data = binascii.a2b_base64(binary_file_content)
        stream = io.BytesIO(data)
        self.file_content.save(random_file_name, stream, save=True)
        self.file_name = random_string
        self.save()

    def delete_file(self):
        filename = self.file_content.path
        if os.path.exists(filename) and os.path.isfile(filename):
            os.remove(filename)

    @property
    def url(self):
        return self.file_content.url

    def __str__(self):
        return "Brand-{1} image-{2}".format(self.pk, self.category_id, self.category_image_id)
