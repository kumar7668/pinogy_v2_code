from django.contrib import admin
from cms.admin.pageadmin import PageAdmin
from cms.models import Page

from .utils import send_page_data_to_api

class CustomPageAdmin(PageAdmin):
    """
    Overrides this class to send the page data to POS when page is moved
    """
    def move_page(self, request, object_id, extra_context=None):
        # Call the original move_page method
        response = super().move_page(request, object_id, extra_context=extra_context)

        send_page_data_to_api()
        
        # Return the original response
        return response


admin.site.unregister(Page)
admin.site.register(Page, CustomPageAdmin)