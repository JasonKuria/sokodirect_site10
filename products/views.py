from django.shortcuts import render
from .models import Product  # import your model
from .forms import ProductForm    # import the form

def products(request):
    # Replace the filler list with a real database query
    products = Product.objects.all()

    context = {'products': products}
    return render(request, 'products/products.html', context)

def create_product(request):
    form = ProductForm()          # instantiate (create) the form

    context = {'form': form}
    return render(request, 'products/product-form.html', context)


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
