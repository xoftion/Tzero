import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_registration_api():
    client = APIClient()
    url = reverse('api_register')
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword123',
        'role': 'BUYER'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert User.objects.count() == 1
    assert User.objects.get().email == 'test@example.com'

@pytest.mark.django_db
def test_user_login_api():
    client = APIClient()
    # First, create a user
    user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')

    # Then, try to log in
    url = reverse('token_obtain_pair')
    data = {
        'email': 'test@example.com',
        'password': 'testpassword123'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_current_user_api_view():
    client = APIClient()
    user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')

    # Get token
    login_url = reverse('token_obtain_pair')
    login_data = {'email': 'test@example.com', 'password': 'testpassword123'}
    login_response = client.post(login_url, login_data, format='json')
    token = login_response.data['access']

    # Access 'me' endpoint
    me_url = reverse('me')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = client.get(me_url)

    assert response.status_code == 200
    assert response.data['email'] == user.email
    assert response.data['username'] == user.username
