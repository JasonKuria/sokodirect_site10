from rest_framework import serializers
from products.models import Product, Category, Review
from users.models import Profile

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'        

#serializer will help us convert our class or table int a jason object
class ProductSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False) #nest relationships
    categories = CategorySerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    #create a method for this class
    def get_reviews(self, obj):
        reviews =obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)

        return serializer.data 