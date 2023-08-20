from django.contrib import admin
from cart.models import Cart, CartItem

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price']
    list_editable = ['total_price']  # Corrected attribute name

admin.site.register(CartItem)
admin.site.register(Cart, CartAdmin)  # Corrected the order and syntax
