from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.getSupportPage, name='support-page'),
]
