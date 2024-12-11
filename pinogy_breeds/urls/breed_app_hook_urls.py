from django.urls import path
from django.views.decorators.cache import never_cache

from pinogy_breeds import views

app_name= "pinogy_breeds"

urlpatterns = [
        path("", never_cache(views.BreedsView.as_view()), name='breed_home'), # All types of breeds
        path("<slug:pet_type_slug>/", never_cache(views.BreedsView.as_view()), name='breed_pet_type'), # Pet type specific breeds
        path("<slug:pet_type_slug>/<slug:breed_slug>/", never_cache(views.BreedDetailView.as_view()), name='breed_detail'), # Breed Detail
]