# products/forms.py

from django.forms import ModelForm
from django import forms
from .models import Product, Review, Category


class ProductForm(forms.ModelForm):
    """
    Form for creating and updating products.
    Includes custom styling and category filtering.
    """
    
    class Meta:
        model = Product
        fields = [
            'county', 'title', 'description', 'price',
            'quantity_available', 'unit', 'featured_image',
            'contact_link', 'farm_link', 'categories'
        ]

    def __init__(self, *user_args, **user_kwargs):
        """
        Initialize the form with custom styling and category filtering.
        """
        super(ProductForm, self).__init__(*user_args, **user_kwargs)

        # 1. Style every input control field uniformly using clean classes
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input-styled-field'})

        # 2. Refine the query selection logic: Only show the leaf (deepest) subcategories
        # so users cannot mistakenly tag a whole generic root tier container.
        self.fields['categories'].queryset = Category.objects.filter(children__isnull=True)
        self.fields['categories'].label = "Select Produce Sub-Categories"


class ReviewForm(ModelForm):
    """
    Form for submitting product reviews with upvote/downvote.
    """
    
    class Meta:
        # Specify which model to use and which fields to include in the form
        model = Review
        fields = ['value', 'body']
        
        # Custom labels for the form fields
        labels = {
            'value': 'Place your vote',
            'body': 'Add a review with your vote'
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with custom styling.
        args: positional arguments passed to the parent init function
        kwargs: keyword arguments passed to the parent init function
        """
        super(ReviewForm, self).__init__(*args, **kwargs)
        
        # Apply CSS class 'input' to each form field for styling purposes
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class CategoryManagementForm(forms.ModelForm):
    """
    Form for managing product categories (admin only).
    Allows creation of both root and sub-categories.
    """
    
    class Meta:
        model = Category
        fields = ['name', 'parent']
        
        # Specify the labels for the form fields to make them more user-friendly
        labels = {
            'name': 'New Category / Sub-Category Name',
            'parent': 'Assign Parent Category (Leave blank if creating a Main Top-Level Category)',
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with custom styling and parent category options.
        """
        super(CategoryManagementForm, self).__init__(*args, **kwargs)
        
        # Apply clean, uniform styling to match your marketplace look
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input-styled-field'})
        
        # Display the choice list using the clean ancestral paths from your __str__ method
        self.fields['parent'].queryset = Category.objects.all().order_by('name')
        self.fields['parent'].empty_label = "--- No Parent (Root Category Tier) ---"