from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import  User
from django.db.models import Q # Import the Q object for complex queries
from .models import Profile, Speciality
from django.contrib import messages
#from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, ProfileForm, SpecialityForm
from .utils import searchProfiles, paginateProfiles


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
        #username_input = request.POST.get('username').strip()
        username_input = request.POST.get('username').strip().lower()
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
            #return redirect('profiles') 

            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        
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
            #return redirect('profiles')
            return redirect('edit-account') # Redirect new users to the profile edit page immediately after registration to encourage them to complete their profile setup. 
        else:
            messages.error(
                request, "An error occurred during account creation.")
            
    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles, search_query = searchProfiles(request) # Call the searchProfiles utility function to retrieve the filtered profiles and the search query. This allows the view to display the relevant profiles based on the user's search input and also pass the search query back to the template for display in the search input field.

    profiles, custom_range = paginateProfiles(request, profiles, 1) # Call the paginateProfiles utility function to paginate the filtered profiles. This allows the view to display a subset of profiles per page and also pass a custom range for pagination links to the template.
    

    # Get the search query from the URL parameters, defaulting to an empty string if not provided
    #search_query = ''

    #if request.GET.get('search_query'): # Extract that querry parameter from the URL and store it in the search_query variable. This allows the view to filter the profiles based on the user's search input.
    #    search_query = request.GET.get('search_query')

    #print("Search Query", search_query) # Debugging statement to verify that the search query is being captured correctly from the URL parameters.        

    #speciality = Speciality.objects.filter(name__icontains=search_query) # Perform a case-insensitive exact match search on the 'name' field of the Speciality model to find a speciality that matches the search query. The first matching speciality is stored in the 'speciality' variable, which is then used to filter profiles based on their associated specialities.

    #profiles = Profile.objects.filter(name__icontains=search_query) # Perform a case-insensitive search on the 'name' field of the Profile model to filter profiles that contain the search query. The resulting queryset is stored in the 'profiles' variable, which is then passed to the template for rendering.
    #profiles = Profile.objects.filter(
    #    name__icontains=search_query, short_intro__icontains=search_query) # Perform a case-insensitive search on both the 'name' and 'short_intro' fields of the Profile model to filter profiles that contain the search query in either field. The resulting queryset is stored in the 'profiles' variable, which is then passed to the template for rendering.
    #profiles = Profile.objects.distinct().filter( # Perform a case-insensitive search on both the 'name' and 'short_intro' fields of the Profile model to filter profiles that contain the search query in either field. The resulting queryset is stored in the 'profiles' variable, which is then passed to the template for rendering.
    #    Q(name__icontains=search_query) | 
    #    Q(short_intro__icontains=search_query) | 
    #    Q(speciality__in=speciality)) # Filter profiles based on their associated specialities that match the search query. This allows users to find profiles not only by name and introduction but also by the specialities they offer.
    

    #profiles = Profile.objects.all()    

    # Renders the users(farmer) profiles listing page
    # Will query Profile.objects.all() once model is built
    context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)

def user_Profile(request, pk):
    profile = Profile.objects.get(id=pk)

    # Speciality with a description
    #topSpeciality = profile.speciality_set.exclude(description__exact="")
    # 1. Top Specialties: Exclude BOTH null values and empty strings
    #topSpeciality = profile.speciality_set.exclude(description__isnull=True).exclude(description__exact="")
    # 1. Top Specialties: Has a description (Excludes both Null values and empty strings)
    topSpeciality = Speciality.objects.filter(owner=profile).exclude(description__isnull=True).exclude(description__exact="")

    # Speciality without a description
    #otherSpeciality = profile.speciality_set.filter(description="")
    # 2. Other Specialties: Get rows where description is EITHER null or an empty string
    #otherSpeciality = profile.speciality_set.filter(description__isnull=True) | profile.speciality_set.filter(description="")
    # 2. Other Specialties: Has no description (Gets rows where description is EITHER null or an empty string)
    otherSpeciality = Speciality.objects.filter(owner=profile, description__isnull=True) | Speciality.objects.filter(owner=profile, description="")
    
    context = {'profile': profile, 
               'topSpeciality': topSpeciality, 
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

@login_required(login_url='login') # Enforces that only authenticated users can access the editAccount view, redirecting unauthenticated users to the login page. 
def editAccount(request):
    """
    Renders the form to edit profile details and processes updates.
    """
    profile = request.user.profile # Extract profile for the current user session
    
    # Pre-populate the form with the current record instance
    form = ProfileForm(instance=profile) # instance=profile-> prefill the fields with the existing data from the profile instance
    
    if request.method == 'POST':
        # Bind incoming data and file attachments to the existing record
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Redirect the user safely back to their dashboard hub
            return redirect('account')
            
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)    

@login_required(login_url='login') 
def createSpeciality(request):
    profile = request.user.profile # Extract profile for the current user session
    form = SpecialityForm()

    if request.method == 'POST':
        form = SpecialityForm(request.POST)
        if form.is_valid():
            speciality = form.save(commit=False) # Hold the new speciality instance in memory before saving to the database
            speciality.owner = profile # Set the owner of the speciality to the current user's profile
            speciality.save() # Save the speciality instance to the database
            messages.success(request, "Speciality added successfully!")
            return redirect('account') # Redirect back to the user's account page after creating a new speciality
        
    context = {'form': form}
    return render(request, 'users/speciality_form.html', context)


@login_required(login_url='login') 
def updateSpeciality(request, pk):
    profile = request.user.profile # Extract profile for the current user session
    speciality = profile.speciality_set.get(id=pk) # Get the specific speciality instance that belongs to the user's profile using the primary key from the URL
    form = SpecialityForm(instance=speciality) # Pre-populate the form with the existing speciality data for editing

    if request.method == 'POST':
        form = SpecialityForm(request.POST, instance=speciality) # Bind the submitted data to the existing speciality instance for update
        if form.is_valid():
            form.save() # Save the speciality instance to the database
            messages.success(request, "Speciality updated successfully!")
            return redirect('account') # Redirect back to the user's account page after creating a new speciality
        
    context = {'form': form}
    return render(request, 'users/speciality_form.html', context)

def deleteSpeciality(request, pk):
    profile = request.user.profile # Extract profile for the current user session
    speciality = profile.speciality_set.get(id=pk) # Get the specific speciality instance that belongs to the user's profile using the primary key from the URL

    if request.method == 'POST':
        speciality.delete() # Delete the speciality instance from the database
        messages.success(request, "Speciality deleted successfully!")
        return redirect('account') # Redirect back to the user's account page after deleting the speciality
    
    context = {'object': speciality} # Pass the speciality instance to the template for confirmation
    return render(request, 'delete-template.html', context)