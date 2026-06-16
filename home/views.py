from django.shortcuts import render

def getHomePage(request):
    return render(request, 'home/home.html')
 
# The template path: 'app_name/filename.html'
# App name first, then the filename.
# This is why the inner folder must match the app name.


