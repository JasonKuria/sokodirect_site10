from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.getAboutPage, name='about-page'),
]
