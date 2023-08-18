from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to="restuarants/",blank=True,null=True)
    
    def __str__(self):
        return self.name
    

class DishCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="dish_categories/",blank=True,null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Dish Categories"
    

class Dish(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(DishCategory, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='dish_images/', null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Dishes"

    def get_restaurant(self):
        return self.restaurant


