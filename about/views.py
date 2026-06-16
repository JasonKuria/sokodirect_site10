from django.shortcuts import render
def getAboutPage(request):
    return render(request, 'about/about.html')

# Create your views here.
