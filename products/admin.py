from django.contrib import admin
from .models import Product    # import your model

# Register it so it shows in the admin panel
admin.site.register(Product)
