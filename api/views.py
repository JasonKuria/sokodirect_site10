from django.http import JsonResponse

#tell us all the urls paths we have
def getRoutes(request):

    #python list
    routes = [
        {'GET':'api/products'}, #Return a list of products objects
        {'GET':'api/products/id'}, #Return a SINGLE product object
        {'POST':'api/products/vote'}, #THIS WILL take a POST method

        {'GET':'/api/users/token'},
        {'GET':'/api/users/token/refresh'},        
    ]

    return JsonResponse(routes, safe=False)