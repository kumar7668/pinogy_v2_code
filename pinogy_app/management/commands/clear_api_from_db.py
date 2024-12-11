from django.core.cache import cache
from django.core.management.base import BaseCommand

from pos_api.ipo_client import IPOClient
from pos_api.models import PoApiSession
from pinogy_breeds.models import ApiBreedPhoto, ApiBreedBadgePhoto
from pinogy_pet.models import ApiPetTypePhoto
from pos_api.models.pet import ApiPetPhoto
from carousel_plugins.models import BrandImage as CarouselBrandImage, PromotionImage as CarouselPromotionImage
from pinogy_shop.models.images import BrandImage, CategoryImage, ProductImage


class Command(BaseCommand):
    help = 'Cleanup the unused media files from ap_media and temp directory'

    def handle(self, *args, **options):
        api_data_models = (
            ApiBreedPhoto, ApiBreedBadgePhoto, ApiPetTypePhoto, ApiPetPhoto, CarouselBrandImage, CarouselPromotionImage,
            BrandImage, CategoryImage, ProductImage
        )
        for media_model in api_data_models:
            media_model.objects.order_by('pk').delete()

        session = PoApiSession.get_solo()
        session.token = ''
        session.save()
        cache.clear()
        client = IPOClient()
        client.login()
