from django.urls import path
from django.views.decorators.cache import never_cache

from pinogy_pet.views import pet_views

app_name= "pinogy_pet"

urlpatterns = [
        path('pet-collection-form/', never_cache(pet_views.PetCollectionFormView.as_view()), name='pet_collection_form'),
        
        path("", never_cache(pet_views.PetTypeView.as_view()), name='pet_type_home'), # All types of pets
        path("<slug:pet_type_slug>/", never_cache(pet_views.PetlistView.as_view()), name='pet_type'), # Pet List
        path("<slug:pet_type_slug>/<slug:breed_slug>/", never_cache(pet_views.PetlistView.as_view()), name='breeds_pet_type'), # Breed wise Pet List

        path("<slug:pet_type_slug>/location/<slug:location_slug>/", never_cache(pet_views.PetlistView.as_view()), name='pet_type_location'), # Pet List - Location wise
        path("<slug:pet_type_slug>/<slug:breed_slug>/location/<slug:location_slug>/", never_cache(pet_views.PetlistView.as_view()), name='breeds_pet_type_location'), # Breed wise Pet List - Location wise
        
        path("<slug:pet_type_slug>/<slug:breed_slug>/<int:pet_id>/", never_cache(pet_views.PetDetailView.as_view()), name='pet_detail'), # Pet type specific Pet
        path('<slug:pet_type_slug>/<slug:breed_slug>/<int:pet_id>/adopt/', never_cache(pet_views.AdoptMeView.as_view()), name='adopt_me'),

]