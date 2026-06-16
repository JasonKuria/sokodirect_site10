from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.getContactPage, name='contact-page'),
]
