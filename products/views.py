from django.shortcuts import render
def getProductsPage(request):
    return render(request, 'products/products.html')

# Create your views here.
