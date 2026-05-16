from django.shortcuts import render

products_list = [
    {
        'id': '1',
        'title': 'Fresh Tomatoes',
        'description': 'Farm fresh tomatoes from Kirinyaga County',
        'price': 'KES 50 per kg',
        'quantity': '500kg available',
    },
    {
        'id': '2',
        'title': 'Sukuma Wiki (Kale)',
        'description': 'Organic kale grown in Limuru',
        'price': 'KES 30 per bunch',
        'quantity': '200 bunches available',
    },
    {
        'id': '3',
        'title': 'Irish Potatoes',
        'description': 'Grade A potatoes from Nyandarua',
        'price': 'KES 80 per kg',
        'quantity': '1 tonne available',
    },
]

def products(request):
    context = {
        'page': 'Products',
        'products': products_list    # pass list into template
    }
    return render(request, 'products/products.html', context)



#def products(request):
#    context = {
#        'page': 'Products',
#        'message': 'Welcome to SokoDirect — Fresh produce from Kenyan farmers'
#    }    
    #return render(request, 'products/products.html')
#    return render(request, 'products/products.html', context)



#def single_product(request, pk):
#    return render(request, 'products/single-product.html')

def single_product(request, pk):
    product_obj = None    # start with nothing found

    # Search the list for product whose id matches URL pk
    for i in products_list:
        if i['id'] == pk:
            product_obj = i    # found it — store it
            break

    context = {'product': product_obj}
    return render(request, 'products/single-product.html', context)





    