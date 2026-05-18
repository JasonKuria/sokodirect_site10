from django.forms import ModelForm
from .models import Product     # import the model


class ProductForm(ModelForm):
    class Meta:
        model = Product         # which model to build the form from
        fields = '__all__'      # generate fields for EVERY attribute
