from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login
from django.shortcuts import render, redirect
from app_authentication.forms import SignUpForm
from django.contrib.auth.models import User
from app_authentication.models import UserAccount

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            address = form.cleaned_data.get('address')
            phone_number = form.cleaned_data.get('phone_number')
            profile_picture = form.cleaned_data.get('profile_picture')

            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()

            user_account = UserAccount.objects.create(user=user)

            if address:user_account.address=address
            if phone_number:user_account.phone_number=phone_number
            if profile_picture:user_account.profile_picture=profile_picture
            user_account.save()
            return redirect('index')  # Redirect to the desired page after successful signup
    else:
        form = SignUpForm()
    return render(request, 'app_authentication/signup.html', {'form': form})



