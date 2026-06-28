from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import Profile


def signup_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()
            role = form.cleaned_data["role"]
            Profile.objects.create(user=user, role=role)
            login(request, user)

            if role == "farmer":
                return redirect("/farmer/dashboard/")
            else:
                return redirect("/buyer/dashboard/")

    else:

        form = RegisterForm()

    return render(
        request,
        "users/signup.html",
        {"form": form}
    )


def login_view(request):

    form = LoginForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            identifier = form.cleaned_data["identifier"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=identifier,
                password=password
            )

            if user:
                login(request, user)
                profile = Profile.objects.get(user=user)

                if profile.role == "farmer":
                    return redirect("/farmer/dashboard/")
                else:
                    return redirect("/buyer/dashboard/")

            messages.error(
                request,
                "Invalid login credentials."
            )

    return render(
        request,
        "users/login.html",
        {"form": form}
    )