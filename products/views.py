from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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

@login_required(login_url='login')
def create_product(request):

    # get the logged-in user's profile
    # you have to be logged in to create a product, so we can safely assume request.user is valid
    # so that we associate each created product with the user who created it
    profile = request.user.profile 

    # C — Create: show empty form on GET, save on POST
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES) # ← add request.FILES
        if form.is_valid():
            product = form.save(commit=False)  # create product object but don't save to DB yet
            product.owner = profile  # set the owner to the logged-in user's profile
            form.save()
            return redirect('products')

    context = {'form': form}
    return render(request, 'products/product-form.html', context)

@login_required(login_url='login')
def update_product(request, pk):

    profile = request.user.profile  # get logged-in user's profile

    # U — Update: pre-fill form with existing product, save changes on POST
    #product = Product.objects.get(id=pk)
    product = profile.product_set.get(id=pk) # only allow updating products owned by the logged-in user
    form = ProductForm(instance=product)   # pre-fill with existing data

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product) # ← add request.FILES
        if form.is_valid():
            form.save()
            return redirect('products')

    context = {'form': form}
    return render(request, 'products/product-form.html', context)

@login_required(login_url='login')
def delete_product(request, pk):

    profile = request.user.profile  # get logged-in user's profile

    # D — Delete: show confirmation on GET, delete on POST
    #product = Product.objects.get(id=pk)
    product = profile.product.set.get(id=pk) # only allow deleting products owned by the logged-in user

    if request.method == 'POST':
        product.delete()
        return redirect('products')

    context = {'object': product}
    return render(request, 'products/delete-template.html', context)


