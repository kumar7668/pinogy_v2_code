from django.urls import path

from .views import ThemeChangeView, ThemeImageView

urlpatterns = [
    path("", ThemeChangeView.as_view(), name="theme-change"),
    path("themeimageview/", ThemeImageView.as_view(), name="themeimage-url"),
]
