from django.test import TestCase
from django.urls import resolve
from .models import Product
from .views import home

# Create your tests here.


class HomeTest(TestCase):
    def setUp(self):
        self.url = '/'
        self.shoe = Product.objects.create(
            name="Fancy Shoe", description="A very fancy shoe.", price=55000, category="shoes")

    def test_view(self):
        page = resolve(self.url)
        self.assertEqual(page.func, home)

    def test_shows_products(self):
        response = self.client.get(self.url)
        self.assertContains(response.context["products"], self.shoe)
