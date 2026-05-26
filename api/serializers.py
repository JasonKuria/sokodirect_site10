from rest_framework import serializers
from products.models import Product

#serializer will help us convert our class or table int a jason object
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'