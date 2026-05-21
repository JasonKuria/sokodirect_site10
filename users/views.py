from django.shortcuts import render

def profiles(request):
    # Renders the users(farmer) profiles listing page
    # Will query Profile.objects.all() once model is built
    context = {}
    return render(request, 'users/profiles.html', context)
