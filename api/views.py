#from django.http import JsonResponse, permission_classes
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ProductSerializer
from products.models import Category, Product

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
@permission_classes([IsAuthenticated]) #only authenticated users can access this endpoint, if not authenticated, they will receive a 401 Unauthorized response.
def getProducts(request):
    #print('USER:', request.user) #request.user will give us the user object of the currently authenticated user making the request. This is useful for logging, debugging, or implementing user-specific logic in the view.
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def removeCategory(request):
    categoryId = request.data['categoryId']
    productId = request.data['productId']

    product = Product.objects.get(id=productId)
    category = Category.objects.get(id=categoryId)

    product.categories.remove(category) # Remove the category from the product's categories. This will disassociate the category from the product without deleting either object from the database.

    return Response('Category was deleted')