from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to="restuarants/",blank=True,null=True)
    is_featured = models.BooleanField(default=False)
    
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

class Sales(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    discount_percentage = models.PositiveIntegerField(validators=[MaxValueValidator(99)])
    start_date = models.DateField()
    end_date = models.DateField()
    dishes = models.ManyToManyField(Dish, related_name='sales', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    
    class Meta:
        verbose_name_plural = "Sales"

    def get_truncated_description(self):
        if len(self.description) > 80:
            return self.description[:80]
        return self.description
    
    def save(self, *args, **kwargs):
        today = timezone.now().date()
        self.is_active = self.start_date <= today <= self.end_date
        super().save(*args, **kwargs)

    
        