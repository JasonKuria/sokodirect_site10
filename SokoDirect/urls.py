from django.contrib import admin
from django.urls import path, include
from django.conf import settings                   # access settings variables
from django.conf.urls.static import static         # builds URL for media files
from django.contrib.auth import views as auth_views #

urlpatterns = [
    path('admin/', admin.site.urls),

    # Users app - empty string = homepage
    # Visiting the root domain shows users(farmer) profiles
    path('', include('users.urls')),

    # Products app - now lives under /products/
    # All product URLs are prefixed with products/
    path('products/', include('products.urls')),

    path('api/', include('api.urls')),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"), name="password_reset_complete"),
]

# Append media URL route — tells Django how to serve uploaded files
# MEDIA_URL = the URL prefix (/media/)
# MEDIA_ROOT = the disk folder where files are stored
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


