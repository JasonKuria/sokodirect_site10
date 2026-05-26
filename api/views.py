from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from products.models import Product

#tell us all the urls paths we have
@api_view(['GET'])
def getRoutes(request):

    #python list
    routes = [
        {'GET':'api/products'}, #Return a list of products objects
        {'GET':'api/products/id'}, #Return a SINGLE product object
        {'POST':'api/products/vote'}, #THIS WILL take a POST method

        {'GET':'/api/users/token'},
        {'GET':'/api/users/token/refresh'},        
    ]

    #return JsonResponse(routes, safe=False)
    return Response(routes)


#@api_view(['GET'], ['POST'])
@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)