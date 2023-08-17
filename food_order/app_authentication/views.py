from django.shortcuts import render

# Create your views here.
def signup(request):
    return render(request,"app_authentication/signup.html")


def login(request):
    return render(request,"app_authentication/login.html")