# tests.py
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

User = get_user_model()

class AuthViewSetTests(APITestCase):
    def setUp(self):
        # Create a user for login tests
        self.register_url = reverse('auth-register')
        self.login_url = reverse('auth-login')

    def test_register_user_success(self):
        # Test user registration with valid data
        data = {
            "username": "newuser",
            "password": "newpassword123",
            "email": "newuser@example.com"
        }
        response = self.client.post(self.register_url, data)
        
        # Check that user registration was successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["username"], data["username"])
        
        # Ensure the user was created and a token was generated
        user = User.objects.get(username=data["username"])
        token_exists = Token.objects.filter(user=user).exists()
        self.assertTrue(token_exists)

    def test_register_user_invalid_data(self):
        # Test registration with missing required fields
        data = {
            "username": "incompleteuser"
        }
        response = self.client.post(self.register_url, data)
        
        # Check that registration failed due to missing email
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_success(self):
        # Test user login with correct credentials
        username = "testuser"
        password = "testpassword"

        self.user = User.objects.create_user(
            username=username, 
            password=password, 
            email="testuser@example.com"
        )
        data = {
            "username": username,
            "password": password,
        }
        response = self.client.post(self.login_url, data)
        
        # Check that login was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_user_invalid_credentials(self):
        # Test login with incorrect password
        data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data)
        
        # Check that login failed due to invalid credentials
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Invalid credentials")

    def test_login_user_nonexistent(self):
        # Test login with a non-existent user
        data = {
            "username": "nonexistentuser",
            "password": "somepassword"
        }
        response = self.client.post(self.login_url, data)
        
        # Check that login failed for a non-existent user
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Invalid credentials")
