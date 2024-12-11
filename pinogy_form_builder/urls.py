from django.urls import path

from .views import BuilderFormSubmitView

app_name= "pinogy_form_builder"

urlpatterns = [
    path('submit-builder-form/', BuilderFormSubmitView.as_view(), name='submit-builder-form'),
]