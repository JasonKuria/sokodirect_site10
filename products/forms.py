from django.forms import ModelForm
from .models import Product
class ProductForm(ModelForm):
    class Meta:
        model = Product

        # Only show fields a farmer needs to fill in
        # vote_total and vote_ratio are calculated automatically
        fields = [
            'title',
            'description',
            'price',
            'quantity_available',
            'unit',
            'county',
            'categories',
            'contact_link',
            'farm_link',
            'featured_image',
        ]
