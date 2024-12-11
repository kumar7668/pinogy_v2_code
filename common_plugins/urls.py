from django.urls import path
from django.conf.urls import url
from common_plugins import views
from .views import google_maps_proxy

app_name= "pinogy_common_ajax"

urlpatterns = [
        path("collection-form/", views.CollectionFormView.as_view(), name='collection_form'),
        path("subscribe-us/", views.SubscribeUsFormView.as_view(), name='subscribe_us_form'),
        path("unsubscribe-us/", views.UnSubscribeUsFormView.as_view(), name='unsubscribe_us_form'),
        path("marketing_notification/", views.MarketingNotification.as_view(), name='marketing_notification'),
        path("schedule_playdate/", views.Playdate.as_view(), name='playdate'),
        path("playDateCreateView_form/", views.PlayDateCreateView.as_view(), name='playDateCreateView_form'),
        path("available_puppy_collection_form/", views.AvailablePuppyCollectionFormView.as_view(), name='available_puppy_collection_form'),
        path('check_zip', views.CheckZipView.as_view(), name='check-zip'),
        path("customer_verification/", views.CustomerVerificationFormView.as_view(), name='customer_verification'),
        path("otp_verification/", views.OtpVerificationFormView.as_view(), name='otp_verification'),
        path("header_delete/", views.HeaderDeleteView.as_view(), name='header-delete-url'),
        path('google-maps-proxy/', google_maps_proxy, name='google_maps_proxy'),
]