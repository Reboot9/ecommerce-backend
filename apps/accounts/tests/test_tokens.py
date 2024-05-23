"""
Test module for token-related functionality using SimpleJWT.

Test cases cover scenarios related to token expiration, rotation, and
refresh token validity.
"""
import logging
from datetime import datetime

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class TokenTestCase(APITestCase):
    """Test JWT API."""

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

    def test_obtain_token(self):
        """Test token obtaining with provided email and password."""
        url = reverse("token_obtain_pair")
        response = self.client.post(url, self.user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

        # Ensure that the access token expires within the configured lifetime
        refresh_token = RefreshToken(response.data["refresh"])
        expiration_timestamp = refresh_token["exp"]

        # Ensure that expiration timestamp is greater than the current time
        self.assertGreater(expiration_timestamp, datetime.now().timestamp())

    def test_refresh_token(self):
        """Obtain the initial access token."""
        token_obtain_url = reverse("token_obtain_pair")
        response = self.client.post(token_obtain_url, self.user_data, format="json")
        access_token = response.data["access"]
        refresh_token = response.data["refresh"]

        # Refresh the access token using the refresh token
        token_refresh_url = reverse("token_refresh")
        data = {"refresh": refresh_token}
        response = self.client.post(token_refresh_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

        # Assert that new refresh token is provided too because of blacklist enabled
        self.assertIn("refresh", response.data)

        new_access_token = RefreshToken(response.data["refresh"]).access_token

        # Ensure that the new access token is different from the initial one
        self.assertNotEqual(access_token, new_access_token)

        # # Ensure that the new access token expires within the configured lifetime
        expiration_timestamp = new_access_token["exp"]
        self.assertGreater(expiration_timestamp, datetime.now().timestamp())

    def test_invalid_refresh_token(self):
        """Attempt to refresh with an invalid refresh token."""
        url = reverse("token_refresh")
        response = self.client.post(url, {"refresh": "invalid_refresh_token"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_obtain_token_for_nonexistent_user(self):
        """Attempt to obtain a token for a nonexistent user."""
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"email": "nonexistent@user.com", "password": "invalidpassword"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
