from django.urls import path
from . import views

urlpatterns = [
    # Farmer profiles listing - will be the homepage
    path('', views.profiles, name='profiles'),
]
