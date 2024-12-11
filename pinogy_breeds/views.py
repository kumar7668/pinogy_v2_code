from django.shortcuts import render
from django.views.generic.base import TemplateView

from pinogy_breeds.pos_api import BreedDetail,PetTypeList

class BreedsView(TemplateView):
    template_name = 'pinogy_breeds/breed_app_hook.html'
    
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get(self, request, pet_type_slug = None, *args, **kwargs):
        
        
        context = {
            'selected_pet_type_slug' : pet_type_slug,
            'breed_page': True
        }
        
        return render(request, self.template_name, context)
    
class BreedDetailView(TemplateView):
    template_name = 'pinogy_breeds/breed_detail_app_hook.html'
    
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get(self, request, pet_type_slug=None, breed_slug=None, *args, **kwargs):
        
        breed_obj = BreedDetail()
        breed_detail = breed_obj.get_breed_data(breed_slug=breed_slug)

        show_pet_type_link = True
        pet_types_obj = PetTypeList()
        pet_types_list = pet_types_obj.get_pet_type_list(None)
        
        if len(pet_types_list) == 1:
            show_pet_type_link = False
        
        context = {
            'selected_pet_type_slug' : pet_type_slug,
            'selected_breed_slug': breed_slug,
            'selected_breed_data': breed_detail,
            'breed_page': True,
            'show_pet_type_link': show_pet_type_link,
        }
        
        return render(request, self.template_name, context)