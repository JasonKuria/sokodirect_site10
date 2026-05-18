from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm


def products(request):
    # R — Read: get all products from the database
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'products/products.html', context)


def single_product(request, pk):
    # R — Read: get one specific product and its related data
    product = Product.objects.get(id=pk)
    reviews = product.review_set.all()    # all reviews for this product
    context = {'product': product, 'reviews': reviews}
    return render(request, 'products/single-product.html', context)

def create_product(request):
    # C — Create: show empty form on GET, save on POST
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')

    context = {'form': form}
    return render(request, 'products/product-form.html', context)


def update_product(request, pk):
    # U — Update: pre-fill form with existing product, save changes on POST
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)   # pre-fill with existing data

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')

    context = {'form': form}
    return render(request, 'products/product-form.html', context)


def delete_product(request, pk):
    # D — Delete: show confirmation on GET, delete on POST
    product = Product.objects.get(id=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('products')

    context = {'object': product}
    return render(request, 'products/delete-template.html', context)


