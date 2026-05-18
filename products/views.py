from django.shortcuts import render
from .models import Product  # import your model

def products(request):
    # Replace the filler list with a real database query
    products = Product.objects.all()

    context = {'products': products}
    return render(request, 'products/products.html', context)

def single_product(request, pk):
    # Get the specific product by its primary key from URL
    product = Product.objects.get(id=pk)

    # Get its categories (ManyToMany)
    categories = product.categories.all()
    # Get its reviews (children via reverse FK)
    reviews = product.review_set.all()

    context = {
        'product': product,
        'categories': categories,
        'reviews': reviews,
    }
    return render(request, 'products/single-product.html', context)
