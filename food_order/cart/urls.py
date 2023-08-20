from django.urls import path
from cart.views import view_cart,add_to_cart,remove_from_cart,update_cart

urlpatterns=[
    path("view_cart",view_cart,name="view_cart"),
    path("update_cart/<int:cart_item_id>",update_cart,name="update_cart"),
    path("add_to_cart/<int:dish_id>",add_to_cart,name="add_to_cart"),
    path("remove_from_cart/<int:cart_item_id>",remove_from_cart,name="remove_from_cart"),
]