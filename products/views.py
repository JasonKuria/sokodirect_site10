from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
#from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm
from .utils import searchProducts

def products(request):
    products, search_query = searchProducts(request) # Call the searchProducts utility function to retrieve the filtered products and the search query. This allows the view to display the relevant products based on the user's search input and also pass the search query back to the template for display in the search input field.
    
    #search_query = ''

    #if request.GET.get('search_query'): 
    #    search_query = request.GET.get('search_query')

    #category = Category.objects.filter(name__icontains=search_query) # Perform a case-insensitive search on the 'name' field of the Category model to find categories that match the search query. The resulting queryset is stored in the 'category' variable, which is then used to filter products based on their associated categories.        

    #products = Product.objects.distinct().filter(
    #    Q(title__icontains=search_query) | 
    #    Q(description__icontains=search_query) | 
    #    Q(owner__name__icontains=search_query) | # Allow searching by the owner's name as well, which is a common requirement in marketplace applications where users may want to find products by specific sellers. This enhances the search functionality by enabling users to find products not only by their title and description but also by the name of the seller, making it easier to discover products from preferred sellers or brands.
    #    Q(categories__in=category) # Filter products based on their associated categories that match the search query. This allows users to find products not only by title and description but also by the categories they belong to, making it easier to discover products within specific categories of interest.
    #)

    # R — Read: get all products from the database
    #products = Product.objects.all()
    context = {'products': products, 'search_query': search_query} # Pass the search query back to the template so that it can be displayed in the search input field, allowing users to see their current search term and modify it if needed.
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
            return redirect('account')

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
            return redirect('account')

    context = {'form': form}
    return render(request, 'products/product-form.html', context)

@login_required(login_url='login')
def delete_product(request, pk):

    profile = request.user.profile  # get logged-in user's profile

    # D — Delete: show confirmation on GET, delete on POST
    #product = Product.objects.get(id=pk)
    product = profile.product_set.get(id=pk) # only allow deleting products owned by the logged-in user

    if request.method == 'POST':
        product.delete()
        return redirect('products')

    context = {'object': product}
    return render(request, 'delete-template.html', context)


