import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Product, Category

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_seller():
    return User.objects.create_user(
        username='testseller',
        email='seller@example.com',
        password='testpassword',
        role='SELLER'
    )

@pytest.fixture
def test_product(test_seller):
    category = Category.objects.create(name='Test Category')
    return Product.objects.create(
        seller=test_seller,
        category=category,
        title='Test Product',
        description='A test description.',
        price_usd=99.99
    )

@pytest.mark.django_db
def test_product_list_api(api_client, test_product):
    url = reverse('product-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) > 0
    assert response.data[0]['title'] == 'Test Product'

@pytest.mark.django_db
def test_product_detail_api(api_client, test_product):
    url = reverse('product-detail', kwargs={'slug': test_product.slug})
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['title'] == test_product.title
    assert response.data['price_usd'] == '99.99'
