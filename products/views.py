# products/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from .forms import ProductForm, ReviewForm, CategoryManagementForm
from .utils import searchProducts, paginateProducts

# from orders.models import Order  # Import your new e-commerce order model
# from orders.utils import cartData  # Import your new e-commerce utility function for cart data


def products(request):
    """
    Display all products with search and pagination
    """
    products, search_query = searchProducts(request)
    products, custom_range = paginateProducts(request, products, 3)
    
    # --- FIXED E-COMMERCE INTEGRATION ---
    # Call cartData utility to seamlessly parse logged-in OR guest cart states
    # 1. Fetch the cookie data total and item count for navbar badge display
    # data = cartData(request)
    # cart_items_count = data['cartItems']
    # order = data['order']

    context = {
        'products': products,
        'search_query': search_query,
        'custom_range': custom_range,
        # 'cartItems': cart_items_count,  # <--- Add this line!
        # 'order': order
    }
    return render(request, 'products/products.html', context)


def single_product(request, pk):
    """
    Display a single product with review form
    """
    productObj = Product.objects.get(id=pk)
    form = ReviewForm()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = productObj
            review.owner = request.user.profile
            review.save()
            productObj.getVoteCount
            
            messages.success(request, 'Your review was submitted successfully!')
            return redirect('single-product', pk=productObj.id)
    
    # --- FIXED E-COMMERCE INTEGRATION ---
    # Dynamically tracking user vs guest sessions for detail layout display metrics
    # data = cartData(request)
    # cart_items_count = data['cartItems']
    # order = data['order']

    context = {
        'product': productObj,
        'form': form,
        # 'cartItems': cart_items_count,  # <--- Add this line!
        # 'order': order
    }
    return render(request, 'products/single-product.html', context)


@login_required(login_url='login')
def create_product(request):
    """
    Create a new product listing
    Only logged-in users can create products
    """
    profile = request.user.profile
    form = ProductForm()
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = profile
            product.save()  # Saves core instance
            
            form.save_m2m()  # Crucial! Saves clean, non-duplicated ManyToMany records safely.
            
            # --- AUTOMATIC ROLE UPGRADE ENGINE ---
            if not profile.is_farmer:
                profile.is_farmer = True
                profile.save()  # Persists the new status in the database
            
            # Add user feedback message before redirecting
            messages.success(request, "Produce AD published successfully!")
            return redirect('account')
    
    context = {'form': form}
    return render(request, 'products/product-form.html', context)


@login_required(login_url='login')
def update_product(request, pk):
    """
    Update an existing product
    Only the owner can update their products
    """
    profile = request.user.profile
    product = profile.product_set.get(id=pk)
    form = ProductForm(instance=product)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()  # Automatically updates core information and ManyToMany associations
            messages.success(request, "Product updated successfully!")
            return redirect('account')
    
    context = {
        'form': form,
        'product': product
    }
    return render(request, 'products/product-form.html', context)


@login_required(login_url='login')
def delete_product(request, pk):
    """
    Delete a product
    Only the owner can delete their products
    """
    profile = request.user.profile  # get logged-in user's profile
    product = profile.product_set.get(id=pk)  # only allow deleting products owned by the logged-in user
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect('products')
    
    context = {'object': product}
    return render(request, 'delete-template.html', context)


@login_required(login_url='login')
def manage_categories(request):
    """
    Manage product categories
    Restricted to administrators or verified managers
    """
    # Restrict this portal view to administrators or verified managers
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Only marketplace administrators can manage category architecture.')
        return redirect('account')
    
    form = CategoryManagementForm()
    
    if request.method == 'POST':
        form = CategoryManagementForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Successfully registered structural tier: "{category}"')
            return redirect('manage-categories')
    
    # Fetch root records only; our template will cascade down through children branches automatically
    root_categories = Category.objects.filter(parent__isnull=True).prefetch_related('children__children')
    
    context = {
        'form': form,
        'root_categories': root_categories
    }
    return render(request, 'products/manage-categories.html', context)