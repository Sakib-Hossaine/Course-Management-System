from django.shortcuts import render


# Home Page View
def home(request):
    return render(request, "home.html")


# Log In Page View
def login(request):
    return render(request, "auth/login.html")


# Sign Up Page View
def signup(request):
    return render(request, "auth/signup.html")
