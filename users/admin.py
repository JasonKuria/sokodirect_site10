from django.contrib import admin
from .models import Profile, Speciality

# Register so they appear in the admin panel
admin.site.register(Profile)
admin.site.register(Speciality)
