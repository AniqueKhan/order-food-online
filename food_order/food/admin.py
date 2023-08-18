from django.contrib import admin
from food.models import Dish,DishCategory,Restaurant
# Register your models here.
admin.site.register((Dish,DishCategory,Restaurant))