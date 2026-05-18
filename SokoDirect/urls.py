from django.contrib import admin
from django.urls import path, include
from django.conf import settings                   # access settings variables
from django.conf.urls.static import static         # builds URL for media files


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
]

# Append media URL route — tells Django how to serve uploaded files
# MEDIA_URL = the URL prefix (/media/)
# MEDIA_ROOT = the disk folder where files are stored
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

