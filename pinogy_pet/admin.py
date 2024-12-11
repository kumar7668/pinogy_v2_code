from django.contrib import admin
from .models import ApiPetBadgePhoto

# Register your models here.
class ApiPetBadgePhotoAdmin(admin.ModelAdmin):
    list_display = ('id','file_name','file_image','file_id','alt','order_updated_at')
    search_fields = ['id','file_name','file_image','file_id','alt','order_updated_at']

admin.site.register(ApiPetBadgePhoto,ApiPetBadgePhotoAdmin)