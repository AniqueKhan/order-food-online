from django.urls import path
from app_authentication.views import signup,profile,edit_profile
from django.contrib.auth import views as authViews 
urlpatterns = [
    path("signup",signup,name='signup'),
    path("profile",profile,name='profile'),
    path("edit_profile",edit_profile,name='edit_profile'),
    path('login', authViews.LoginView.as_view(template_name='app_authentication/login.html'), name='login'),
    path('logout', authViews.LogoutView.as_view(), {'next_page' : 'index'}, name='logout'),
]
