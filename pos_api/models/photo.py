import binascii
import datetime
import io
import os
from random import choice
from string import ascii_uppercase

from typing import Dict, List, Optional
from django.core.files import File
from django.db import models
from django.utils.translation import ugettext_lazy as _
from PIL import Image

BASE_PHOTO_IMAGE_WIDTH = 1000

temp_dir = "C:/work/builder/pinogy-new-base/data/media" 
media_location = "C:/work/builder/pinogy-new-base/data/media"


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


def create_dir(f):
    os.makedirs(os.path.dirname(f))
    
class BasePhotoManager(models.Manager):
    
    def get_images_from_api(self, client, file_ids: List[int], model_default: Dict[str, any] = None, non_defaults: Dict[str, any] = None):
        
        """Get images from API based on give file Ids

        Args:
            client : PWAPI Object
            file_ids: List of POS file ids
            model_default: Default value for model (is not included in lookups)
            non_defaults: fields those must be included in lookups (ex. pet_id)
                        : keys must be same as model fields name 
        
        Returns:
            List of objects of self class
        """
        
        items = client.post_queries(
            **{
                "quippet_name": "read__tbl__vw_files_with_in_band_contents",
                "quippet_params": {"qp_file_id": ",".join(str(item) for item in file_ids)},
            }
        )["objects"]

        if non_defaults is None:
            non_defaults = {}

        result = []
        for item in items:
            item_obj, created = self.get_or_create(
                file_id=item["file_id"], defaults=model_default, **non_defaults
            )
            if created:
                file_data = item["flin_contents"].encode("utf-8")
                item_obj.file_extension = item["file_orig_extension"]
                item_obj.alt = item["file_description"]
                item_obj.save()
                item_obj.save_file(file_data)
                result.append(item_obj)
        return result
    
    def get_images(self, client, api_images_data: List[Dict[str, any]], model_defaults: Dict[str, any] = None, model_filters: Optional[Dict[str, any]] = None, non_defaults: Optional[Dict[str, any]] = None, default_image: bool = True) -> List[Dict[str, any]]:
        """
        1. Filter out images from db based on given ``model_filters``
        2. Create a photo_set based on db result
        3. iterate trough ``api_images_data`` and check if image available or not
            if available in DB then add image url in result
            if not available in DB then fetch it from db using ``get_images_from_api``
        4. Sort the results and return it

        Args:
            client (PWAPI): PWAPI Object
            api_images_data (List[Dict[str, any]]): Images metadata from POS
            model_defaults (Dict[str, any]): Default values for models
            model_filters (Optional[Dict[str, any]], optional): Default values for filter the images
            non_defaults (Optional[Dict[str, any]], optional): Non Defaults fields values
            default_image (bool, optional): False if expect blank list incase images not available

        Returns:
            List of images
            image_object = {
                'order': 0,
                "alt": "alt_text",
                'image_url': 'image_url'
            }
        """
           
        # if api_images_data is not available and default_images true than return placeholder image
        # else return blank list  
        if not api_images_data and default_image:
            return [{
                'order': 0,
                "alt": "Placeholder image",
                'image_url': '/static/images/default-placeholder-image.webp'
            }]
        elif not api_images_data:
            return []
        
        model_defaults = model_defaults or {}
        non_defaults = non_defaults or {}
        model_filters = model_filters or {}

        available_images = self.filter(**model_filters)
        photo_set = {image.file_id : image for image in available_images}
        
        result = []
        for api_image_meta in api_images_data:
            image = {
                "order": api_image_meta.get('sort_order', 0),
                "alt": api_image_meta['file']['description'],
            }
            
            if api_image_meta['file']['id'] in photo_set:
                image["image_url"] = photo_set[api_image_meta['file']['id']].url
            else:
                model_defaults["order"] = image['order'] or 0  # set the order 0 if the value is coming None from API
                api_image = self.get_images_from_api(client, [api_image_meta['file']['id']], model_defaults, non_defaults)
                if not api_image: 
                    continue
                image["image_url"] = api_image[0].url
            
            result.append(image)
        
        sorted_result = sorted(result, key=lambda image: image['order'])
        
        return sorted_result
    
    def get_pet_badges(self, client, api_badges_data: List[Dict[str, any]]):
        """
        1. Get all the pet badges from DB
        2. Create a photo_set based on db result
        3. iterate trough ``api_badges_data`` and check if image available or not
            if available in DB then add image url in result
            if not available in DB then fetch it from db using ``get_images_from_api``

        Args:
            client (PWAPI): PWAPI Object
            api_images_data (List[Dict[str, any]]): Badges metadata from POS

        Returns:
            List of images
            image_object = {
                "alt": "alt_text",
                'image_url': 'image_url'
            }
        """

        available_badges = self.all()
        photo_set = {image.file_id : image for image in available_badges}
        
        result = []
        for api_image_meta in api_badges_data:
            image = {
                "alt": api_image_meta['badge_name'],
            }
            
            if api_image_meta['badge_file_id'] in photo_set:
                image["image_url"] = photo_set[api_image_meta['badge_file_id']].url
            else:
                model_defaults = {
                    'height': 76,
                    'width': 76
                }
                api_image = self.get_images_from_api(client, [api_image_meta['badge_file_id']], model_defaults)
                if not api_image: 
                    continue
                image["image_url"] = api_image[0].url
            
            result.append(image)
                
        return result


class BasePhoto(models.Model):
    ORDER_UPDATE_DELAY = datetime.timedelta(hours=1)

    photo = models.TextField(default=None, blank=True, null=True)
    size = (650, 650)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    file_name = models.CharField(max_length=300, blank=True, null=True, default=None)

    file_extension = models.CharField(
        _("file_extension"), max_length=32, blank=True, null=True, default=None
    )
    file_image = models.ImageField(upload_to="ap_media")
    file_id = models.IntegerField(_("remote file ID"), blank=True, default=0)
    alt = models.CharField(max_length=300, blank=True, null=True, default=None)
    width = models.IntegerField(_("Image file width"), blank=True, default=0)
    height = models.IntegerField(_("Image file height"), blank=True, default=0)
    order_updated_at = models.DateTimeField(auto_now_add=True)
    
    objects = BasePhotoManager()

    class Meta:
        abstract = True

    def save_file(self, photo=None):
        try:
            random_string = "".join(choice(ascii_uppercase) for _ in range(12))
            random_file_name = "{0}.{1}".format(random_string, self.file_extension)

            if photo:
                data = binascii.a2b_base64(photo)
            else:
                data = binascii.a2b_base64(self.photo)
            stream = io.BytesIO(data)

            img_pil = Image.open(stream)

            if self.height and self.width:
                img_pil = img_pil.resize(
                    (self.width, self.height), Image.ANTIALIAS
                )
            else:
                wpercent = BASE_PHOTO_IMAGE_WIDTH / float(img_pil.size[0])
                image_height = int((float(img_pil.size[1]) * float(wpercent)))
                img_pil = img_pil.resize(
                    (BASE_PHOTO_IMAGE_WIDTH, image_height), Image.ANTIALIAS
                )
                self.width = BASE_PHOTO_IMAGE_WIDTH
                self.height = image_height

            img_pil.save(temp_dir + random_file_name, quality=30)

            stored_image = open(temp_dir + random_file_name, "rb")
            img = File(stored_image)
            self.file_image.save(random_file_name, img, save=True)
            self.file_name = random_string
            self.save()
            stored_image.close()
        except FileNotFoundError:
            create_dir(temp_dir)
            create_dir(media_location)
            self.save_file(photo=photo)
        except Exception as e:
            print("➡ Exception :", e)
            self.delete()

    def url(self):
        if self.file_name:
            return self.file_image.url
        else:
            pass

    def original_location(self):
        if self.file_name:
            return "data/media/ap_media/{0}.{1}".format(
                self.file_name, self.file_extension
            )
        else:
            pass

    def delete_file(self):
        if not self.file_name:
            return
        ensure_dir(temp_dir)
        ensure_dir(media_location)
        file_media_location = (
            media_location + self.file_name + "." + self.file_extension
        )
        file_temp_location = temp_dir + self.file_name + "." + self.file_extension
        try:
            if os.path.isfile(file_media_location):
                os.remove(file_media_location)
            if os.path.isfile(file_temp_location):
                os.remove(file_temp_location)
        except Exception as e:
            print("➡ Exception :", e)
