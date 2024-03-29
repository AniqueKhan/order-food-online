from django import forms
from django.contrib.auth.models import User
from app_authentication.models import UserAccount
from django.utils import timezone
from datetime import timedelta

class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=30, required=True)
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}), max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True, label="Confirm your password.")
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),max_length=20,required=False)
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-2'}),max_length=255,required=False)
    profile_picture = forms.ImageField(required=False)

    def clean(self):
        super(SignUpForm,self).clean()
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if User.objects.filter(username=username).exists():
            self.add_error("username","Username already exists.")
        if User.objects.filter(email=email).exists():
            self.add_error("email","Email already exists.")

        if password != confirm_password:
            self.add_error("password","The Passwords do not match. Please try again.")
        return self.cleaned_data


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['address', 'phone_number', 'profile_picture','balance']

    def clean(self):
        super(EditProfileForm,self).clean()
        profile = self.instance

        if profile.last_balance_added is not None and (timezone.now() - profile.last_balance_added <= timedelta(days=1)):
            self.add_error("balance", "You can only update your balance once a day.")
        else:
            profile.last_balance_added = timezone.now()
        return self.cleaned_data