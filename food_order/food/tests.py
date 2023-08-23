from django.test import TestCase
from food.models import Restaurant,Dish,DishCategory,Sales
from decimal import Decimal
from datetime import date,timedelta
from django.core.exceptions import ValidationError
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

