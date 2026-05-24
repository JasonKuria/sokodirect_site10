from .models import Product, Category
from django.db.models import Q # Import the Q object for complex queries

def searchProducts(request):
    search_query = ''

    if request.GET.get('search_query'): 
        search_query = request.GET.get('search_query')

    category = Category.objects.filter(name__icontains=search_query) # Perform a case-insensitive search on the 'name' field of the Category model to find categories that match the search query. The resulting queryset is stored in the 'category' variable, which is then used to filter products based on their associated categories.        

    products = Product.objects.distinct().filter(
        Q(title__icontains=search_query) | 
        Q(description__icontains=search_query) | 
        Q(owner__name__icontains=search_query) | # Allow searching by the owner's name as well, which is a common requirement in marketplace applications where users may want to find products by specific sellers. This enhances the search functionality by enabling users to find products not only by their title and description but also by the name of the seller, making it easier to discover products from preferred sellers or brands.
        Q(categories__in=category) # Filter products based on their associated categories that match the search query. This allows users to find products not only by title and description but also by the categories they belong to, making it easier to discover products within specific categories of interest.
    )


    return products, search_query