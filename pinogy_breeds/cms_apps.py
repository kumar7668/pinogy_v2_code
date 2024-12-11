from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class BreedsApphook(CMSApp):
    name = "Pinogy Breeds"
    app_name = "pinogy_breeds"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["pinogy_breeds.urls.breed_app_hook_urls", ]


apphook_pool.register(BreedsApphook)