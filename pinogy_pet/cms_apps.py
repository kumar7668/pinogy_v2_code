from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class PetsApphook(CMSApp):
    name = "Pinogy pet"
    app_name = "pinogy_pet"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["pinogy_pet.urls.pets_app_hook_urls", ]


apphook_pool.register(PetsApphook)

