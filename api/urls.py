from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, # Refresh the access token using the refresh token
)

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Endpoint to refresh the access token using the refresh token usually 30 days 
    # after the access token expires, the user can use the refresh token to get a 
    # new access token without re-authenticating.
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 

    path('', views.getRoutes),
    path('products/', views.getProducts),
    path('product/<str:pk>', views.getProduct),    
]