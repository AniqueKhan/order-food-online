from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from app_authentication.forms import SignUpForm,EditProfileForm
from django.contrib.auth.models import User
from app_authentication.models import UserAccount
from cart.models import Cart

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

            cart = Cart.objects.create(user=user)
            cart.save()

            user_account = UserAccount.objects.create(user=user)

            if address:user_account.address=address
            if phone_number:user_account.phone_number=phone_number
            if profile_picture:user_account.profile_picture=profile_picture
            user_account.save()
            return redirect('index')  # Redirect to the desired page after successful signup
    else:
        form = SignUpForm()
    return render(request, 'app_authentication/signup.html', {'form': form})


@login_required
def profile(request):
    profile = UserAccount.objects.filter(user=request.user).first()
    context = {
        "profile":profile
    }
    return render(request,"app_authentication/profile.html",context)

@login_required
def edit_profile(request):
    profile = UserAccount.objects.get(user=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after successful update
    else:
        form = EditProfileForm(instance=profile)

    context = {
        'form': form
    }
    return render(request, 'app_authentication/edit_profile.html', context)