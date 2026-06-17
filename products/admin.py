from django.contrib import admin
#from .models import Product, Review, Category, County, Profile, Message, Speciality
from .models import Product, Review, Category, County, Message, Speciality

# Register all models
admin.site.register(Product)      # ← only once
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(County)
#admin.site.register(Profile)      # ← add these missing ones
admin.site.register(Message)
admin.site.register(Speciality)