# Register your models here.
from django.contrib import admin
from .models.pet import ApiPetPhoto

class ApiPetPhotoAdmin(admin.ModelAdmin):
    list_display = ('id','file_name','file_image', 'pet_id', 'file_id','alt','order_updated_at')
    search_fields = ['id','file_name','file_image', 'pet_id', 'file_id','alt','order_updated_at']

admin.site.register(ApiPetPhoto, ApiPetPhotoAdmin)