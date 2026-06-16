from django.shortcuts import render
def getSupportPage(request):
    return render(request, 'support/support.html')

# Create your views here.
