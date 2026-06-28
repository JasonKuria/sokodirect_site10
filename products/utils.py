# products/utils.py

from .models import Product, Category
from django.db.models import Q  # Import the Q object for complex queries
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProducts(request, products, results):
    """
    Paginate products for display in templates.
    
    Args:
        request: The HTTP request object
        products: The queryset of products to paginate
        results: Number of results per page
    
    Returns:
        tuple: (paginated_products, custom_range)
    """
    # Get the 'page' parameter from the GET request.
    # If it's not provided, default to 1.
    page = request.GET.get('page', 1)
    
    # Number of products to display per page
    results = 6
    
    # Create a Paginator object with the filtered products and the number of results per page
    paginator = Paginator(products, results)
    
    try:
        # Get the products for the current page
        products = paginator.page(page)
    except PageNotAnInteger:
        # If the 'page' parameter is not an integer, default to the first page
        page = 1
        products = paginator.page(page)
    except EmptyPage:
        # If the 'page' parameter is out of range, default to the last page
        page = paginator.num_pages
        products = paginator.page(page)
    
    # Calculate the left index for pagination links.
    # This will determine how many page numbers to show before the current page.
    leftIndex = int(page) - 4
    if leftIndex < 1:
        leftIndex = 1  # Ensure the left index does not go below 1
    
    # Calculate the right index for pagination links.
    # This will determine how many page numbers to show after the current page.
    rightIndex = int(page) + 5
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1  # Ensure the right index does not go beyond the total number of pages
    
    # Create a custom range for pagination links.
    # This can be used in the template to display page numbers for navigation.
    custom_range = range(leftIndex, rightIndex)
    
    return products, custom_range


def searchProducts(request):
    """
    Search products by title, description, owner name, and categories.
    
    Args:
        request: The HTTP request object
    
    Returns:
        tuple: (filtered_products, search_query)
    """
    search_query = ''
    
    # Get the search query from the GET request
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    # Perform a case-insensitive search on the 'name' field of the Category model
    # to find categories that match the search query.
    category = Category.objects.filter(name__icontains=search_query)
    
    # Filter products based on multiple criteria:
    # - Title contains the search query
    # - Description contains the search query
    # - Owner's name contains the search query (enables finding products by specific sellers)
    # - Categories match the search query (allows discovering products within specific categories)
    products = Product.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(categories__in=category)
    )
    
    return products, search_query