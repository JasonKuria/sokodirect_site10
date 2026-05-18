from django.urls import path
from . import views
urlpatterns = [
    path('', views.products, name='products'),
    path('product/<str:pk>/', views.single_product, name='single-product'),

    # New — form page for adding a produce listing
    path('create-product/', views.create_product, name='create-product'),
]