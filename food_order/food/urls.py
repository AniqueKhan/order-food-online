from django.urls import path
from food.views import index,restaurants,search,dish_categories,category_detail,restaurant_detail,sale_detail
urlpatterns = [
    path("",index,name='index'),
    path("restaurants",restaurants,name='restaurants'),
    path("search",search,name='search'),
    path("dish_categories",dish_categories,name='dish_categories'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
    path('sale/<int:sale_id>/', sale_detail, name='sale_detail'),
    path('restaurant/<int:restaurant_id>/', restaurant_detail, name='restaurant_detail'),
]