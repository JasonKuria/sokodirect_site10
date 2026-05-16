from django.shortcuts import render


def products(request):
    return HttpResponse('Here is all our produce')

def single_product(request, pk):
    return HttpResponse('Single produce item: ' + pk)
