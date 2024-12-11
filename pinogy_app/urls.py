from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path ,re_path

from . import views

admin.autodiscover()

urlpatterns = [
    re_path(r'^resetpassword/', views.redirect_reset, name='reset_entry_point'),
    
    path('api/sitemap-data/', views.SitemapDataAPI.as_view(), name='sitemap-data-api'),
    path('webhook/sitemap/', views.SiteMapWebhook.as_view(), name='sitemap-webhook'),
    path("sitemap.xml/", views.get_sitemap_view, name='sitemap'),
    
    path("robots.txt/", include('robots.urls')),
    
    path(".well-known/pki-validation/<str:file_name>/", views.readFileview, name='SSLValidation'),
    
    path("taggit_autosuggest/", include('taggit_autosuggest.urls')),
    
    path("admin/clearcache/", include("pinogy_cache.urls")),
    path("admin/", admin.site.urls),
    
    path("theme/", include("custom_design.urls")),
    
    path("health/check/", views.health_check, name="health-check"),
    
    path("common_plugins_ajax/", include("common_plugins.urls")),
    
    path("pet-purchase/", include("pinogy_pet.urls.pet_purchase_urls")),
    
    path("form-builder/", include("pinogy_form_builder.urls")),
    
    path("shop/", include('pinogy_shop.urls.proxi_urls')),

    path("unsubscribe/",  views.UnSubscribePlugin.as_view(), name='unsubscribe'),
    
    path("ml_subscribe/",  views.Subscribe.as_view(), name='ml_subscribe'),

    path("", include("cms.urls")),
]


# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
