from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import  User
from .models import Profile
from django.contrib import messages

def loginUser(request):
    # Authorization Restriction: Active users shouldn't see the login page
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username_input = request.POST.get('username').strip()
        password_input = request.POST.get('password')
        
        # 1. Validation Step: Explicitly verify if the username exists
        try:
            user_exists = User.objects.get(username=username_input)
        except User.DoesNotExist:
            messages.error(request, "Account username does not exist.")
            return render(request, 'users/login_register.html')

        # 2. Authentication Step: Check if password string matches hashes
        # The authenticate function will return None if the password is incorrect, 
        # even if the username exists
        user = authenticate(request, username=username_input, password=password_input)
        
        if user is not None:
            login(request, user) # Provisions active session cookies
            messages.success(request, f"Welcome back to SokoDirect, {user.username}!")
            # Redirects user to the homepage to the profiles listing page after successful login
            # or the previously page they were trying to access before being prompted to login
            return redirect('profiles') 
        else:
            messages.error(request, "Username Or password Incorrect. Please try again.")

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request) # Destroys active backend and browser session cookies
    messages.info(request, "You have successfully logged out of your session.")
    return redirect('login')


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


