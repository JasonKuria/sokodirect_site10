from django.shortcuts import render
 
def getContactPage(request):
    return render(request, 'contact/contact.html')

# Create your views here.
