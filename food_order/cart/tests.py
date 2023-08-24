from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from food.models import Dish, Sales,Restaurant
from cart.models import Cart, CartItem
from datetime import date,timedelta

class CartViewTests(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="Test Restaurant")
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.cart = Cart.objects.create(user=self.user)
        self.dish = Dish.objects.create(name='Test Dish', price=10.00,restaurant=self.restaurant)
        self.sale = Sales.objects.create(
            restaurant=self.restaurant,
            title="Test Sale",
            discount_percentage=20,
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=1),
        )
        self.dish.sales.add(self.sale)
        
    def test_add_to_cart(self):
        url = reverse('add_to_cart', args=[self.dish.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)  # Check if the response redirects
        self.assertEqual(self.cart.cartitem_set.count(), 1)  # Check if the cart item is added
        
    def test_remove_from_cart(self):
        cart_item = CartItem.objects.create(cart=self.cart, dish=self.dish, quantity=2)
        url = reverse('remove_from_cart', args=[cart_item.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)  # Check if the response redirects
        # Try to get the cart item, it should raise a DoesNotExist exception
        with self.assertRaises(CartItem.DoesNotExist):
            CartItem.objects.get(id=cart_item.id)  
        
    def test_update_cart(self):
        cart_item = CartItem.objects.create(cart=self.cart, dish=self.dish, quantity=2)
        url = reverse('update_cart', args=[cart_item.id])
        data = {str(cart_item.id): '3'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)  # Check if the response redirects
        updated_cart_item = CartItem.objects.get(id=cart_item.id)
        self.assertEqual(updated_cart_item.quantity, 3)  # Check if the quantity is updated
        
    def test_view_cart(self):
        url = reverse('view_cart')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)  # Check if the response is successful
        self.assertTemplateUsed(response, 'cart/view_cart.html')  # Check if the correct template is used

