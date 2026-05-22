from django.urls import path
from . import views

urlpatterns = [
    # Farmer profiles listing - will be the homepage
    path('', views.profiles, name='profiles'),

    path('profile/<str:pk>/', views.user_Profile, name='user_profile'),

    # Secure Session Routes
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
]