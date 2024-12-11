from django.db import models
from pos_api.models.photo import BasePhoto
from cmsplugin_cascade.models_base import CascadeModelBase

# Create your models here.
class ApiBreedPhoto(BasePhoto):
    breed_id = models.IntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ("order",)
    
    def __str__(self):
        try:
            return "Api Breed photo: {0}".format(self.photo.file)
        except (AttributeError, ValueError):
            return "Api Breed photo: {0}".format(self.pk)
        
class ApiBreedBadgePhoto(BasePhoto):

    class Meta:
        ordering = ("order",)
    
    def __str__(self):
        try:
            return "Api Breed Badge photo: {0}".format(self.photo.file)
        except (AttributeError, ValueError):
            return "Api Breed Badge photo: {0}".format(self.pk)
        
class BreedDetailPluginModel(CascadeModelBase):
    pass

