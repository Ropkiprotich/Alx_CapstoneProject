from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Product, Category

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Smartphone',
            description='A cool smartphone.',
            price=699.99,
            category=self.category,
            stock_quantity=50
        )
        self.client.login(username='testuser', password='testpass')

    def test_product_list(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_create(self):
        data = {
            'name': 'Laptop',
            'description': 'A powerful laptop.',
            'price': 1200.00,
            'category_id': self.category.id,
            'stock_quantity': 30
        }
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)