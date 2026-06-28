from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile


def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)


def user_Profile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSpeciality = profile.speciality_set.exclude(description__exact="")
    otherSpeciality = profile.speciality_set.filter(description="")
    context = {
        'profile': profile,
        'topSpeciality': topSpeciality,
        'otherSpeciality': otherSpeciality
    }
    return render(request, 'users/user-profile.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_dashboard')   # sends to dashboard after login
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def userDashboard(request):
    profile = request.user.profile

    # Fetch this user's own product listings
    # Will work once your Product model has an `owner` field linked to Profile
    try:
        my_products = profile.product_set.all().order_by('-created')
        total_products = my_products.count()
    except Exception:
        my_products = []
        total_products = 0

    context = {
        'profile': profile,
        'my_products': my_products,
        'total_products': total_products,
        'total_orders': 0,      # placeholder — wire up when orders model exists
        'unread_count': 0,      # placeholder — wire up when inbox model exists
        'profile_views': 0,     # placeholder — wire up when analytics exist
    }
    return render(request, 'users/userDash.html', context)