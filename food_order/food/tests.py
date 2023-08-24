from django.test import TestCase,Client
from food.models import Restaurant,Dish,DishCategory,Sales
from decimal import Decimal
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date,timedelta
from django.core.exceptions import ValidationError
from food.forms import SaleForm
from django.db.utils import IntegrityError

class BaseTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="Test Restaurant")

class RestaurantModelTestCase(BaseTestCase):
    def test_str_representation(self):
        self.assertEqual(str(self.restaurant),"Test Restaurant")


class DishCategoryModelTestCase(TestCase):
    def test_str_representation(self):
        category =DishCategory.objects.create(name="Test Category")
        self.assertEqual(str(category),"Test Category")


class DishModelTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.dish = Dish.objects.create(name="Test Dish",restaurant=self.restaurant,price=10.0)

    def test_str_representation(self):
        self.assertEqual(str(self.dish),"Test Dish")

    def test_get_restaurant_from_dish(self):
        self.assertEqual(self.dish.get_restaurant(),self.restaurant)

    def test_sale_price_calculation(self):

        sale = Sales.objects.create(
            restaurant=self.restaurant,
            title="Test Sale",
            discount_percentage=20,
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=1),
        )
        sale.dishes.add(self.dish)
        sale.save()

        self.dish.refresh_from_db()
        self.assertTrue(self.dish.on_sale)
        self.assertEqual(self.dish.sale_price, Decimal("8.00"))

class SalesModelTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.sale = Sales.objects.create(
            restaurant=self.restaurant,
            title="Test Sale",
            discount_percentage=10,
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=1),
        )

    def test_str_representation(self):
        self.assertEqual(str(self.sale),"Test Sale")

    def test_get_truncated_description(self):
        self.sale.description = """
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Quibusdam hic incidunt quod 
        fugit praesentium error veritatis ad. Magnam, soluta iste blanditiis officiis possimus 
        sint non provident totam facere rem perferendis, ut accusantium, minus nam. Quas aperiam animi 
        velit iure error facere doloremque voluptatum? Quo ullam iure, fugiat error dolorem perferendis 
        qui necessitatibus ad ut quisquam porro. Ipsa iste placeat ullam necessitatibus, eius magni, eveniet 
        saepe accusantium eos, illum adipisci quaerat harum deserunt aliquam? A atque architecto at earum voluptas, 
        ipsum excepturi deleniti, corrupti est distinctio enim odit nulla veniam magni aliquam provident impedit 
        quisquam ducimus consequuntur quia qui ex. Debitis.
        """
        self.sale.save()
        self.assertTrue(len(self.sale.get_truncated_description())<=80)

        self.sale.description = "Lorem ipsum dolor"
        self.sale.save()
        self.assertEqual(self.sale.get_truncated_description(),"Lorem ipsum dolor")


    def test_active_sale(self):
        self.assertTrue(self.sale.is_active)

    def test_inactive_sale(self):
        self.sale.start_date = date.today() + timedelta(days=1)
        self.sale.end_date = date.today() + timedelta(days=2)
        self.sale.save()
        self.assertFalse(self.sale.is_active)

    def test_sale_with_missing_and_wrong_data(self):
        restaurant = Restaurant.objects.create(name="Test Restaurant")
        # Create a Sales instance with missing required fields
        with self.assertRaises(ValidationError):
            Sales.objects.create(
                restaurant=restaurant, 
                title="Invalid Sale",
                start_date=date.today() - timedelta(days=1),
                end_date=date.today() + timedelta(days=1),
            )
        with self.assertRaises(ValidationError):
            Sales.objects.create(
                restaurant=restaurant, 
                title="Invalid Sale",
                discount_percentage=10,
                end_date=date.today() + timedelta(days=1),
            )
        with self.assertRaises(ValidationError):
            Sales.objects.create(
                restaurant=restaurant,
                title="Invalid Sale",
                discount_percentage=10,
                start_date=date.today() - timedelta(days=1),
            )
        with self.assertRaises(IntegrityError):
            Sales.objects.create(
                restaurant=None,
                title="Invalid Sale",
                discount_percentage=10,
                start_date=date.today() - timedelta(days=1),
                end_date=date.today() + timedelta(days=1),
            )

        with self.assertRaises(ValidationError):
            Sales.objects.create(
                restaurant=restaurant,
                title=None,
                discount_percentage=10,
                start_date=date.today() - timedelta(days=1),
                end_date=date.today() + timedelta(days=1),
            )

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.restaurant = Restaurant.objects.create(name="Test Restaurant")
        self.dish_category = DishCategory.objects.create(name="Test Category")
        self.dish = Dish.objects.create(name="Test Dish", restaurant=self.restaurant, price=10.0,category=self.dish_category)
        self.sale = Sales.objects.create(
            restaurant=self.restaurant,
            title="Test Sale",
            discount_percentage=10,
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=1),
        )
        self.sale.dishes.add(self.dish)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Featured Restaurants")
        self.assertContains(response, "Special Sales")

    def test_sale_detail_view(self):
        response = self.client.get(reverse('sale_detail', args=[self.sale.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Sale")
        self.assertContains(response, "Test Dish")

    def test_dish_categories_view(self):
        response = self.client.get(reverse('dish_categories'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Category")

    def test_restaurants_view(self):
        response = self.client.get(reverse('restaurants'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Restaurant")

    def test_restaurant_detail_view(self):
        response = self.client.get(reverse('restaurant_detail', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Restaurant")
        self.assertContains(response, "Test Dish")
        self.assertContains(response, "Test Sale")

    def test_category_detail_view(self):
        response = self.client.get(reverse('category_detail', args=[self.dish_category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Category")
        self.assertContains(response, "Test Dish")


class SaleFormTestCase(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="Test Restaurant")
        self.dish = Dish.objects.create(name="Test Dish", restaurant=self.restaurant, price=10.0)
        self.dish2 = Dish.objects.create(name="Test Dish2", restaurant=self.restaurant, price=10.0)
        self.existing_sale = Sales.objects.create(
            restaurant=self.restaurant,
            title="Existing Sale",
            discount_percentage=15,
            start_date=date.today() - timedelta(days=1),
            end_date=date.today() + timedelta(days=1),
        )
        self.existing_sale.dishes.add(self.dish)

    def test_valid_form(self):
        data = {
            'restaurant': self.restaurant.id,
            'title': 'New Sale',
            'description': 'Test description',
            'discount_percentage': 20,
            'start_date': date.today() - timedelta(days=1),
            'end_date': date.today() + timedelta(days=1),
            'dishes': [self.dish2.id],
        }
        form = SaleForm(data=data)
        self.assertTrue(form.is_valid())



    # def test_invalid_form(self):
    #     data = {
    #         'restaurant': self.restaurant.id,
    #         'title': '',
    #         'description': '',
    #         'discount_percentage': 20,
    #         'start_date': date.today() + timedelta(days=1),
    #         'end_date': date.today() + timedelta(days=2),
    #         'dishes': [self.dish.id],
    #     }
    #     form = SaleForm(data=data)
    #     self.assertFalse(form.is_valid())
    #     print(f'{e}\n' for e in form.errors)
    #     self.assertEqual(len(form.errors), 2)  # Two fields with errors

    # def test_end_date_in_past(self):
    #     data = {
    #         'restaurant': self.restaurant.id,
    #         'title': 'Invalid Sale',
    #         'description': 'Test description',
    #         'discount_percentage': 20,
    #         'start_date': date.today() - timedelta(days=2),
    #         'end_date': date.today() - timedelta(days=1),
    #         'dishes': [self.dish.id],
    #     }
    #     form = SaleForm(data=data)
    #     self.assertFalse(form.is_valid())
    #     self.assertEqual(len(form.errors), 1)

    # def test_dish_not_in_selected_restaurant(self):
    #     data = {
    #         'restaurant': self.restaurant.id,
    #         'title': 'Invalid Sale',
    #         'description': 'Test description',
    #         'discount_percentage': 20,
    #         'start_date': date.today() - timedelta(days=1),
    #         'end_date': date.today() + timedelta(days=1),
    #         'dishes': [self.dish.id],
    #     }
    #     form = SaleForm(data=data)
    #     self.assertFalse(form.is_valid())
    #     self.assertEqual(len(form.errors), 1)

    # def test_existing_active_sale_for_dish(self):
    #     data = {
    #         'restaurant': self.restaurant.id,
    #         'title': 'Invalid Sale',
    #         'description': 'Test description',
    #         'discount_percentage': 20,
    #         'start_date': date.today() - timedelta(days=1),
    #         'end_date': date.today() + timedelta(days=1),
    #         'dishes': [self.dish.id],
    #     }
    #     form = SaleForm(data=data, instance=self.existing_sale)
    #     self.assertFalse(form.is_valid())
    #     self.assertEqual(len(form.errors), 1)