from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login
from django.shortcuts import render, redirect
from app_authentication.forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            print("form is valid")
            return redirect('index')  # Redirect to the desired page after successful signup
    else:
        form = SignUpForm()
    return render(request, 'app_authentication/signup.html', {'form': form})



def login(request):
    return render(request,"app_authentication/login.html")