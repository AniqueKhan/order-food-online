from django.db import models
from django.contrib.auth.models import User
from food.models import Dish

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Dish, through='CartItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Cart for {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.quantity} x {self.dish.name} in {self.cart.user.username}'s cart"

    def save(self, *args, **kwargs):
        self.subtotal = self.dish.sale_price * self.quantity if self.dish.on_sale else self.dish.price * self.quantity
        super().save(*args, **kwargs)
