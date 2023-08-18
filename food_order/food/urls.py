from django.urls import path
from food.views import index,restaurants,dish_categories,category_detail,restaurant_detail
urlpatterns = [
    path("",index,name='index'),
    path("restaurants",restaurants,name='restaurants'),
    path("dish_categories",dish_categories,name='dish_categories'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
    path('restaurant/<int:restaurant_id>/', restaurant_detail, name='restaurant_detail'),
]