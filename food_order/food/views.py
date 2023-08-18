from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from food.models import Restaurant,DishCategory,Dish
from django.db.models import Count
# Create your views here.
@login_required
def index(request):
    featured_restaurants = Restaurant.objects.all() # Change this logic
    context = {
        "featured_restaurants":featured_restaurants
    }
    return render(request,"food/index.html",context)


@login_required
def dish_categories(request):
    dish_categories = DishCategory.objects.annotate(dish_count=Count('dish'))
    context = {
        "dish_categories":dish_categories
    }
    return render(request,"food/dish_categories.html",context)


@login_required
def restaurants(request):
    restaurants = Restaurant.objects.all()
    print(restaurants)
    context = {
        "restaurants":restaurants
    }
    return render(request,"food/restaurants.html",context)

@login_required
def restaurant_detail(request,restaurant_id):
    restaurant = get_object_or_404(Restaurant,id=restaurant_id)
    dishes = Dish.objects.filter(restaurant=restaurant)
    context = {
        "restaurant": restaurant,
        "dishes": dishes
    }
    return render(request, "food/restaurant_detail.html", context)

@login_required
def category_detail(request, category_id):
    category = get_object_or_404(DishCategory, id=category_id)
    dishes = Dish.objects.filter(category=category)
    context = {
        "category": category,
        "dishes": dishes
    }
    return render(request, "food/category_detail.html", context)
