from django.db import models
from pos_api.models.photo import BasePhoto
# from django.utils.encoding import python_2_unicode_compatible
# Create your models here.
from cmsplugin_cascade.models_base import CascadeModelBase
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import JSONField
from cms.models import Page
import json


from django.core.cache import caches
import datetime
from django.utils.translation import (
    ugettext_lazy as _,
    get_language,
    override
)
from .cms_plugins_api_utils import get_list_of_ad_cards, get_ad_card
from django.utils import timezone
try:
    cache = caches['redis']
except:
    cache = caches['default']
    


class ApiPetTypePhoto(BasePhoto):
    pet_type_id = models.IntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ('order', )

    def __str__(self):
        try:
            return "Api Pet Type photo: {0}".format(self.photo.file)
        except (AttributeError, ValueError):
            return "Api Pet Type photo: {0}".format(self.pk)
        
class ApiPetBadgePhoto(BasePhoto):

    class Meta:
        ordering = ("order",)
    
    def __str__(self):
        try:
            return "Api Pet Badge photo: {0}".format(self.photo.file)
        except (AttributeError, ValueError):
            return "Api Pet Badge photo: {0}".format(self.pk)


class ApiPetAdCard(BasePhoto):
    CHOICES = (
        (0, 'Photo'),
        (1, 'Video'),
    )

    file_content = models.FileField(upload_to='ap_media', blank=False, null=False)
    file_type = models.CharField(max_length=255, default=0, choices=CHOICES)
    pet_type_id = models.IntegerField(default=0, blank=False, null=False)
    ad_card_link = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        app_label = 'pinogy_pet'
        ordering = ('order', )

    # def save_file(self, binary_file_content=None):
    #     random_string = ''.join(choice(ascii_uppercase) for _ in range(12))
    #     random_file_name = '{0}.{1}'.format(random_string, self.file_extension)

    #     data = binascii.a2b_base64(binary_file_content)
    #     stream = io.BytesIO(data)
    #     self.file_content.save(random_file_name, stream, save=True)
    #     self.file_name = random_string
    #     self.save()

    # def delete_file(self):
    #     if self.file_content:
    #         if os.path.isfile(self.file_content.path):
    #             os.remove(self.file_content.path)

    @property
    def url(self):
        # return self.file_content.url
        pass

    def get_ad_cards_from_db(pet_type_id):
        cache_key = 'pinogy_available_pets:models.pet:get_ad_cards_from_db:{pet_type_id}'.format(pet_type_id=str(pet_type_id))
        cache_result = cache.get(cache_key)
        if not cache_result:
            cache_result = []
            list_of_ad_cards = get_list_of_ad_cards(pet_type_id=pet_type_id)
            if not list_of_ad_cards:
                ad_cards = ApiPetAdCard.objects.filter(pet_type_id=pet_type_id).all()
                if ad_cards:
                    for ad_card in ad_cards:
                        ad_card.delete()
            else:
                updated_file_ids = []
                for item in list_of_ad_cards:
                    ad_card = ApiPetAdCard.objects.filter(file_id=item['id']).first()
                    if ad_card:
                        ad_card.ad_card_link = item['ad_card_link']
                        ad_card.sort_order = item['sort_order']
                        ad_card.uploaded_at = datetime.datetime.now()
                        ad_card.save()
                    else:
                        ad_card = get_ad_card(file_id=int(item['id']))
                        if ad_card['objects']:
                            file_orig_extension = ad_card['objects'][0]['file_orig_extension']
                            if int(item['file_type']) == 1:
                                ApiPetAdCard.objects.create(
                                    order=item['sort_order'],
                                    file_name=item['url'],
                                    file_extension=file_orig_extension,
                                    file_id=int(item['id']),
                                    pet_type_id=pet_type_id,
                                    file_type=1,
                                    ad_card_link = item['ad_card_link'],
                                )
                            else:
                                flin_contents = ad_card['objects'][0]['flin_contents']
                                new_ad_card = ApiPetAdCard.objects.create(
                                    order=item['sort_order'],
                                    file_name='{}.{}'.format(
                                        ad_card['objects'][0]['file_orig_basename'].replace(' ', '-'),
                                        ad_card['objects'][0]['file_orig_extension']),
                                    file_extension=file_orig_extension,
                                    file_id=int(item['id']),
                                    pet_type_id=pet_type_id,
                                    file_type=0,
                                    ad_card_link=item['ad_card_link'],
                                )
                                new_ad_card.save_file(photo=flin_contents.encode('utf-8'))
                    updated_file_ids.append(int(item['id']))
                cards = ApiPetAdCard.objects.filter(pet_type_id=pet_type_id).all()
                if cards and updated_file_ids:
                    for card in cards:
                        if card.file_id in updated_file_ids:
                            
                            if card.file_type == '1':
                                url = card.file_name 
                            elif card.file_image:
                                url = card.file_image.url
                            else:
                                url = '/static/images/dog-placeholder-img.webp'
                            cache_result.append({
                                'content_type': card.file_type,
                                'url': url,
                                'is_video': True if card.file_type == '1' else False,
                                'ad_card_link': card.ad_card_link if card.ad_card_link not in ['@null', '', None] else '',
                            })
                        else:
                            card.delete()
            cache.set(cache_key, cache_result, 3600)
        return cache_result

    def __str__(self):
        try:
            return "Api pet ad card: {0}".format(self.photo.file)
        except (AttributeError, ValueError):
            return "Api pet ad card: {0}".format(self.pk)
        

class PetDetailPluginModel(CascadeModelBase):

    promob_image = models.ImageField(
        null=True,
        blank=True,
        default=None,
        upload_to="background",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "svg", "webp"]
            )
        ],
    )

    button_data = JSONField(
        null=True,
        blank=True,
        default=None,)
    
    def save(self, *args, **kwargs):
        if isinstance(self.button_data, str):
            self.button_data = json.loads(self.button_data)

        if isinstance(self.button_data, dict):
            for i in range(len(self.button_data)):
                key = f'btn{i+1}'
                if key in self.button_data and 'id_button_internallink' in self.button_data[key]:
                    internallink = self.button_data[key]['id_button_internallink']
                    self.button_data[key]['internallink_id'] = internallink
                    if internallink:
                        try:
                            page = Page.objects.get(id=internallink)
                            self.button_data[key]['button_internallink'] = page.get_absolute_url()
                        except ObjectDoesNotExist:
                            self.button_data[key]['button_internallink'] = None
        
        if isinstance(self.glossary, dict):
            for i in range(len(self.glossary)):
                key = 'btn_type_internal_link'
                if key in self.glossary:
                    internal_link_data = self.glossary[key]
                    if internal_link_data:
                        link_id = internal_link_data.get('pk',None)
                        if link_id:
                            try:
                                page = Page.objects.get(id=link_id)
                                self.glossary[key]['link_path'] = page.get_absolute_url()
                            except ObjectDoesNotExist:
                                self.glossary[key]['link_path'] = None




        

        super(PetDetailPluginModel, self).save(*args, **kwargs)

class PetListPluginModel(CascadeModelBase):
    button_data = JSONField(
        null=True,
        blank=True,
        default=dict)
    
    def save(self, *args, **kwargs):
        if isinstance(self.button_data, str):
            self.button_data = json.loads(self.button_data)
                        
        super(PetListPluginModel, self).save(*args, **kwargs)