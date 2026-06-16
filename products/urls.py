from django.urls import path
from . import views

urlpatterns = [
    path('', views.getProductsPage, name='products-page'),
]

