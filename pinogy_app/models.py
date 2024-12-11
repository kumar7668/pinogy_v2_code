import os

from cmsplugin_cascade.models_base import CascadeModelBase
from django.db import models
from cms.models.pluginmodel import CMSPlugin
from django.core.exceptions import ValidationError


#the method for check the extension of the file and delete the sitemap file if exists
def validate_file_ext(value):
    ext = os.path.splitext(value.name)[1] 
    valid_extensions = ['.xml']
    if ext.lower() not in valid_extensions:
        raise ValidationError(u'Unsupported file extension.') 
    
def get_file_path(instance, filename):
    modified_filename = "sitemap.xml"
    return os.path.join('sitemap', modified_filename)

class SiteMapModel(CMSPlugin):
    document = models.FileField(upload_to = get_file_path, validators=[validate_file_ext], blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            self.delete_file()
        super().save(*args, **kwargs)
    
    def get_file_path(self):
        crd_dir = os.getcwd()
        return f'{crd_dir}/static_collected/media/sitemap/sitemap.xml'

    def delete_file(self):
        file_path = self.get_file_path()
        if os.path.exists(file_path):
            os.remove(file_path)
    
    def __str__(self) -> str:
        return "document"

class Plugin1Model(CascadeModelBase):
    is_show = models.BooleanField(default=False)
