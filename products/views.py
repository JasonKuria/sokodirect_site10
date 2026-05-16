from django.shortcuts import render

def products(request):
    context = {
        'page': 'Products',
        'message': 'Welcome to SokoDirect — Fresh produce from Kenyan farmers'
    }    
    #return render(request, 'products/products.html')
    return render(request, 'products/products.html', context)



def single_product(request, pk):
    return render(request, 'products/single-product.html')




    