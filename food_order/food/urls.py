from django.urls import path
from food.views import index
urlpatterns = [
    path("",index,name='index')
]