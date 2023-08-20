from django.urls import path
from cart.views import view_cart

urlpatterns=[
    path("view_cart",view_cart,name="view_cart")
]