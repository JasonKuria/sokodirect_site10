from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Product, Category
from .forms import ProductForm, ReviewForm
from .utils import searchProducts, paginateProducts

def products(request):
    products, search_query = searchProducts(request) # Call the searchProducts utility function to retrieve the filtered products and the search query. This allows the view to display the relevant products based on the user's search input and also pass the search query back to the template for display in the search input field.
    
    products, custom_range = paginateProducts(request, products, 3) # Call the paginateProducts utility function to paginate the filtered products. This allows the view to display a subset of products based on the pagination settings and also pass a custom range for pagination links to the template.
    

    #page = 1  # Default to the first page
    #page = 2 # Get the 'page' parameter from the GET request. If it's not provided, default to 1. This allows users to navigate through different pages of products.
    #page = request.GET.get('page', page) # Get the 'page' parameter from the GET request. If it's not provided, default to the value of the 'page' variable (which is 2 in this case). This allows users to navigate through different pages of products.
    #results = 3 # Number of products to display per page
    #paginator = Paginator(products, results) # Create a Paginator object with the filtered products and the number of results per page.

    #products = paginator.page(page) # Get the products for the current page. This will return a subset of the products based on the pagination settings.

    #try:
    #    products = paginator.page(page) # Try to get the products for the current page. This will return a subset of the products based on the pagination settings.
    #except PageNotAnInteger:
    #    page = 1 # If the 'page' parameter is not an integer, default to the first page.
    #    products = paginator.page(page) # Get the products for the first page.
    #except EmptyPage:
    #    page = paginator.num_pages # If the 'page' parameter is out of range (e.g., too high), default to the last page.
    #    products = paginator.page(page) # Get the products for the last page.

    #leftIndex = int(page) - 4 # Calculate the left index for pagination links. This will determine how many page numbers to show before the current page.
    #if leftIndex < 1:
    #    leftIndex = 1 # Ensure the left index does not go below 1.
    
    #rightIndex = int(page) + 5 # Calculate the right index for pagination links. This will determine how many page numbers to show after the current page.
    #if rightIndex > paginator.num_pages:
    #    rightIndex = paginator.num_pages + 1 # Ensure the right index does not go beyond the total number of pages.

    #custom_range = range(leftIndex, rightIndex) # Create a custom range for pagination links. This can be used in the template to display page numbers for navigation.

    context = {'products': products, 'search_query': search_query, 'custom_range': custom_range} # Pass the search query back to the template so that it can be displayed in the search input field, allowing users to see their current search term and modify it if needed.
    return render(request, 'products/products.html', context)


def single_product(request, pk):
    # R — Read: get one specific product and its related data
    productObj = Product.objects.get(id=pk)

    #reviews = product.review_set.all()    # all reviews for this product
    form = ReviewForm() # empty form for submitting a new review

    if request.method == 'POST':
        form = ReviewForm(request.POST) # populate form with submitted data
        if form.is_valid():
            review = form.save(commit=False) # create review object but don't save to DB yet
            review.product = productObj # associate review with the current product
            review.owner = request.user.profile # set the owner of the review to the logged-in user's profile
            review.save() # save the review to the database

            # Update the product's vote total and ratio
            productObj.getVoteCount # call the getVoteCount property to update the product's vote_total and vote_ratio fields based on the new review

            messages.success(request, 'Your review was submitted successfully!')
            return redirect('single-product', pk=productObj.id) # redirect to the same product page to show the new review


    context = {'product': productObj, 'form': form} # pass the empty form to the template so that it can be rendered on the product detail page, allowing users to submit new reviews for the product.
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
        newCategories = request.POST.get('newcategories').replace(',', " ").split() # Get the new categories from the POST data, replace commas with spaces, and split into a list. This allows users to enter multiple categories separated by commas or spaces.
        #print("DATA:", newCategories) # Debug: print POST data to console

        form = ProductForm(request.POST, request.FILES) # ← add request.FILES
        if form.is_valid():
            product = form.save(commit=False)  # create product object but don't save to DB yet
            product.owner = profile  # set the owner to the logged-in user's profile
            form.save()

            for cat in newCategories:
                category, created = Category.objects.get_or_create(name=cat) # Get or create a Category object for each category name in the newCategories list. This allows the application to handle both existing and new categories without duplication.
                product.categories.add(category) # Add the category to the product's categories. This establishes the many-to-many relationship between the product and its categories.         

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
        newCategories = request.POST.get('newcategories').replace(',', " ").split() # Get the new categories from the POST data, replace commas with spaces, and split into a list. This allows users to enter multiple categories separated by commas or spaces.
        #print("DATA:", newCategories) # Debug: print POST data to console

        form = ProductForm(request.POST, request.FILES, instance=product) # ← add request.FILES
        if form.is_valid():
            #form.save()
            product = form.save()   
            for cat in newCategories:
                category, created = Category.objects.get_or_create(name=cat) # Get or create a Category object for each category name in the newCategories list. This allows the application to handle both existing and new categories without duplication.
                product.categories.add(category) # Add the category to the product's categories. This establishes the many-to-many relationship between the product and its categories.         
            return redirect('account')

    context = {'form': form, 'product': product}
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


