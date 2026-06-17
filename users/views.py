from django.shortcuts import render
from .models import Profile

def profiles(request):
    profiles = Profile.objects.all()

    # Renders the users(farmer) profiles listing page
    # Will query Profile.objects.all() once model is built
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)

def user_Profile(request, pk):
    profile = Profile.objects.get(id=pk)

    # Speciality with a description
    topSpeciality = profile.speciality_set.exclude(description__exact="")
    # Speciality without a description
    otherSpeciality = profile.speciality_set.filter(description="")
    
    context = {'profile': profile, 'topSpeciality': topSpeciality, 
               'otherSpeciality': otherSpeciality}

    # Renders the user profile page
    return render(request, 'users/user-profile.html', context)
