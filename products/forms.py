from django.forms import ModelForm
from django import forms
from .models import Product, Review


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

class ReviewForm(ModelForm):
    class Meta: # specify which model to use and which fields to include in the form
        model = Review # specify the model to use for this form
        fields = ['value', 'body'] # specify which fields from the model to include in the form, the value field is the rating (up/down) and body is the review text

        label = {
            'value': 'Place your vote',
            'body': 'Add a review with your vote'
        }

    # this function is called to style the form fields when the form is rendered in the template
    # kwargs allows us to pass any number of arguments to the function, 
    # which we then pass to the parent init function
    # args is used to pass any number of positional arguments 
    # to the function, which we also pass to the parent init function
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'}) # add the CSS class 'input' to each form field for styling purposes