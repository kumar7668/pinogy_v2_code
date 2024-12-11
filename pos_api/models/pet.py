from django.db import models

from pos_api.models.photo import BasePhoto

class ApiPetPhotoManager(models.Manager):
    
    def get_pet_image(self, client, pet_id, image_id, order=0):
        """
        save pet image in DB if not available
        return given pet image petimage
        """
        item = client.post_queries(**{
            "quippet_name": 'read__tbl__vw_files_with_in_band_contents',
            "quippet_params": {
                'qp_file_id': image_id
            }
        })['objects'][0]

        model_default = {
            "order": order,
            "pet_id": pet_id,
        }

        item_obj, created = self.get_or_create(file_id=image_id, defaults=model_default)

        if created:
            file_data = item['flin_contents'].encode('utf-8')
            item_obj.file_extension = item['file_orig_extension']
            item_obj.alt = item['file_description']
            item_obj.save()
            item_obj.save_file(file_data)
        
        return item_obj

class ApiPetPhoto(BasePhoto):
    pet_id = models.IntegerField(default=0, blank=False, null=False)
    is_badges = models.BooleanField(default=False)

    image_objects = ApiPetPhotoManager()

    class Meta:
        ordering = ("order",)

    def __str__(self):
        try:
            return "Api Pet photo: {0}".format(self.photo.file)
        except (AttributeError, ValueError):
            return "Api Pet photo: {0}".format(self.pk)
    
