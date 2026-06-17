from django.forms import ModelForm
from django import forms
from .models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'title', 'description', 'price',
            'quantity_available', 'unit',
            'county', 'categories',
            'contact_link', 'farm_link',
            'featured_image',
        ]

        # One way to customise form fields is using widgets — 
        # this allows us to change the default form field type for a model field
        widgets = {
            # Change categories from multi-select list to checkboxes
            # Much more user-friendly — no need to hold Ctrl to select multiple
            'categories': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        # Call the parent init first — required
        super(ProductForm, self).__init__(*args, **kwargs)



        #self.fields['title'].widget.attrs.update({'class': 'input'})

        # Loop through every field in the form
        # Add the theme's CSS class 'input' to every field widget
        # This gives each input the correct styling from app.css
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        # Customise specific fields individually if needed:
        # self.fields['title'].widget.attrs.update({'placeholder': 'e.g. Fresh Tomatoes - Grade A'})
