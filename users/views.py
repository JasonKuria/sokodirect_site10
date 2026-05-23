from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import  User
from .models import Profile
from django.contrib import messages
#from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm


def loginUser(request):
    # Context variable to conditionally render the login form 
    # in the shared login_register.html template
    # what is page for? its used in the login_register.html template 
    # to determine whether to display the login form or the registration form.
    page = 'login' 


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



def registerUser(request):
    # Security Check: Redirect active authenticated accounts away from registration screens
    if request.user.is_authenticated:
        return redirect('profiles')
        
    # Context variable to conditionally render the registration 
    # form in the shared login_register.html template        
    page = 'register' # This variable is used in the login_register.html template to determine whether to display the login form or the registration form.
    form = CustomUserCreationForm()
    
    if request.method == 'POST': # When the registration form is submitted, the view processes the POST request to create a new user account.
        # Bind submitted POST payloads to our customized registration schema class
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            # Commit=False holds a local memory instance of the user before database insertion
            # why we do this is because we want 
            # to perform string normalization on the username field before saving it to the database.
            user = form.save(commit=False)
            
            # String Normalization: Enforce strictly lowercase usernames to eliminate duplicate profile collision exploits
            user.username = user.username.lower()
            user.save() # Formally writes transaction block parameters to disk storage
            
            messages.success(
                request, "Your SokoDirect farmer account was Created successfully!")
            
            # Seamless Onboarding: 
            # Instantly authorize the session cookies without forcing a manual re-login stage
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(
                request, "An error occurred during account creation.")
            
    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)









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


@login_required(login_url='login')
def userAccount(request):
    """
    Renders the secure dashboard workspace for the currently logged-in user.
    Extracts profile assets using the request session token to avoid exposing primary keys in the URL.
    """
    # Use the one-to-one relationship on the logged-in user to fetch their profile
    profile = request.user.profile
    
    # Extract related skills and projects using reverse lookups
    # Speciality with a description
    #topSpeciality = profile.speciality_set.exclude(description__exact="")
    # Speciality without a description
    #otherSpeciality = profile.speciality_set.filter(description="")
    specialities = profile.speciality_set.all()
    products = profile.product_set.all()

    context = {
        'profile': profile,
        'specialities': specialities,
        'products': products
    }
    return render(request, 'users/account.html', context)


