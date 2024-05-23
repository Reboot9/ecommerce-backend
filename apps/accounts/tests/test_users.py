"""
Test module for user-related functionality in a Django Rest Framework API.

Tests cover scenarios related to user registration, retrieving and deletion
"""
import logging

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserAPITestCase(APITestCase):
    """Test CustomUser API."""

    def setUp(self):
        """Set up basic environment for test case."""
        self.user_data = {
            "email": "test@example.com",
            "password": "TestPassword123#",
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=self.user)

        # Reduce the log level to avoid messages like 'bad request'
        logger = logging.getLogger("django.request")
        self.previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

    def tearDown(self) -> None:
        """Reset the log level back to normal."""
        logger = logging.getLogger("django.request")
        logger.setLevel(self.previous_level)

    def test_create_user(self):
        """Test creating account."""
        url = reverse("accounts:user-list")
        data = {
            "email": "i@c.cm",
            "password": "TestPass@",
            "password2": "TestPass@",
        }
        response = self.client.post(url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn("id", response.data["user"])
        self.assertEqual(response.data["user"]["email"], data["email"])
        self.assertIn("createdAt", response.data["user"])
        self.assertIn("updatedAt", response.data["user"])

        self.assertIn("access", response.data["tokens"])
        self.assertIn("refresh", response.data["tokens"])
        self.assertTrue(User.objects.filter(email=data["email"], is_active=True).exists())

    def test_retrieve_user(self):
        """Test retrieving user account."""
        url = reverse("accounts:user-detail", kwargs={"pk": self.user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("id", response.data)
        self.assertEqual(response.data["email"], self.user_data["email"])
        self.assertIn("createdAt", response.data)
        self.assertIn("updatedAt", response.data)

    def test_delete_user(self):
        """Test delete user."""
        url = reverse("accounts:user-detail", kwargs={"pk": self.user.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id, is_active=True).exists())

    def test_create_user_wrong_password_confirm(self):
        """Test user creation with passwords that don't match."""
        url = reverse("accounts:user-list")
        data = {
            "email": "test1@example.com",
            "password": "TestPass",
            "password2": "TestPass1",  # passwords don't match
        }
        response = self.client.post(url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Access error details in the list
        password_error = str(response.data["password"][0])
        password2_error = str(response.data["password2"][0])
        expected_error_message = "Passwords do not match."

        self.assertEqual(password_error, expected_error_message)
        self.assertEqual(password2_error, expected_error_message)
        self.assertFalse(User.objects.filter(email=data["email"], is_active=True).exists())

    def test_create_user_non_latin_password(self):
        """Test user creation with non latin password."""
        url = reverse("accounts:user-list")
        data = {
            "email": "test1@example.com",
            "password": "Пароль1234#",
            "password2": "Пароль1234#",
        }
        response = self.client.post(url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        password_error = str(response.data["password"][0])
        password2_error = str(response.data["password2"][0])
        expected_error_message = (
            "Password must contain only latin letters, numbers, and special characters "
            "(!\"#$%&'()*+,-./:;<>?=@[\\]^_`{|}~)."
        )

        self.assertIn(password_error, expected_error_message)
        self.assertIn(password2_error, expected_error_message)
        self.assertFalse(User.objects.filter(email=data["email"], is_active=True).exists())

    def test_retrieve_user_wrong_id(self):
        """Test retrieving user with an incorrect ID."""
        incorrect_id = 999
        url = reverse("accounts:user-detail", kwargs={"pk": incorrect_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertNotIn("email", response.data)
        self.assertNotIn("createdAt", response.data)
        self.assertNotIn("updatedAt", response.data)

    # def test_xss_vulnerability_on_user_creation(self):
    #     """Test for potential XSS injection vulnerabilities during user creation."""
    #     url = reverse("accounts:user-list")
    #     malicious_script = '<script>alert("XSS Attack!");</script>'
    #     data = {
    #         "email": "xssvulnerability@ex.com",
    #         "password": malicious_script,
    #         "password2": malicious_script
    #     }
    #     response = self.client.post(url, data=data, format='json')
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #
    #     # Check that the response does not contain the injected script
    #     self.assertNotIn(response.data, malicious_script)

    # def test_sql_injection_vulnerability_on_user_creation(self):
    #     """Test for SQL injection vulnerability by injecting malicious SQL."""
    #     url = reverse("accounts:user-list")
    #     malicious_sql = 'test@example.com" OR 1=1; --'
    #     data = {
    #         "email": malicious_sql,
    #         "password": "malicious_password",
    #         "password2": "malicious_password"
    #     }
    #     response = self.client.post(url, data=data, format="json")
    #     print(response.data)
    #     # Ensure that the response does not contain an SQL error message
    #     self.assertNotContains(response, 'SQL', status_code=status.HTTP_400_BAD_REQUEST)
