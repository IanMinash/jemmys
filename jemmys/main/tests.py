from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from djmoney.money import Money
from .models import Product, Order, OrderItem, BuyerAddress, ProductCategory
from .views import make_order

# Create your tests here.


class OrderTest(TestCase):
    def setUp(self):
        self.cloth_cat = ProductCategory.objects.create(category="Clothes")
        self.buyer = BuyerAddress.objects.create(name="Carl Jones", street="Grove St", city="Los Santos",
                                                 region="San Andreas", phone="+1-800-22-56637", email="cj@gsf.gang", country="America")
        self.shoe = Product.objects.create(
            name="Shoe", price=1500, category=self.cloth_cat, quantity=5)
        self.shirt = Product.objects.create(
            name="Shirt", price=900, category=self.cloth_cat, quantity=3)
        self.client = Client()

    def test_qty_reduced_after_order_fulfilled(self):
        order = Order.objects.create(buyer=self.buyer)
        OrderItem.objects.create(order=order, item=self.shoe, quantity=2)
        OrderItem.objects.create(order=order, item=self.shirt, quantity=2)
        self.assertEqual(order.total, Money(5000, 'KES'))
        self.assertEqual(len(Order.objects.all()), 1)
        order.status = 'F'
        order.save()
        self.assertEqual(Product.objects.get(id=self.shoe.id).quantity, 3)
        self.assertEqual(Product.objects.get(id=self.shirt.id).quantity, 1)


class SetSessionTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_session_variable_created(self):
        self.client.post(reverse(
            'set-session'), {'name': 'Cleopatra'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(self.client.session['name'], 'Cleopatra')
        self.client.post(reverse(
            'set-session'), {'city': 'Alexandria'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(self.client.session['city'], 'Alexandria')


class ProductTest(TestCase):
    def setUp(self):
        self.cloth_cat = ProductCategory.objects.create(category="Clothes")
        self.shirt = Product.objects.create(
            name="Shirt", price=900, category=self.cloth_cat, quantity=3)
        self.shirt_but_red = Product.objects.create(
            name="Shirt #2", price=900, category=self.cloth_cat, quantity=1, variant_of=self.shirt, variant_info='Red')

    def test_variant_price_change_on_parent_change(self):
        self.shirt.price = 1200
        self.shirt.save(update_fields=['price'])
        self.shirt_but_red.refresh_from_db()
        self.assertEqual(self.shirt_but_red.price, self.shirt.price)

    def test_variant_category_change_on_parent_change(self):
        new_cat = ProductCategory.objects.create(category="Shirts")
        self.shirt.category = new_cat
        self.shirt.save(update_fields=['category'])
        self.shirt_but_red.refresh_from_db()
        self.assertEqual(self.shirt_but_red.category, new_cat)
