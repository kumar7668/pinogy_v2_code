from django.urls import path

from pinogy_pet.views import pet_purchase

app_name= "pinogy_pet_purchase"

urlpatterns = [
    path('create-txn/', pet_purchase.CreateTransactoin.as_view(), name='create-pet-txn'),
    path('execute-payment/', pet_purchase.ExecutePayment.as_view(), name='execute-pet-payment'),
]