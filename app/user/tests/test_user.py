"""
Tests for the users API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**parama):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**parama)


class PublicUserApiTests(TestCase):
    """Test the public featres of the user API"""
    def setUp(self):
        self.client = APIClient()
        self.payload = {
            "email": "text@example.com",
            "password": "test123#",
            "name": "Test Name"
        }

    def test_create_user_success(self):
        """Test create a user is successful."""
        response = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=self.payload['email'])
        self.assertTrue(user.check_password(self.payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        create_user(**self.payload)
        res = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less then 5 chars."""
        res = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=self.payload['email']
        )
        self.assertFalse(user_exists)
