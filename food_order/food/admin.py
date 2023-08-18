from django.contrib import admin
from food.models import Dish,DishCategory,Restaurant,Sales
from food.forms import SaleForm
# Register your models here.

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name','is_featured']
    list_editable = ['is_featured']

class SalesAdmin(admin.ModelAdmin):
    form=SaleForm
    list_display = ['title',"is_active"]
    # list_editable = ['title']

admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(Sales,SalesAdmin)

admin.site.register((Dish,DishCategory))