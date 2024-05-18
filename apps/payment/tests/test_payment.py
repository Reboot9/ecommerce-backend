"""
Tests related to payment functionality.
"""
import logging
from unittest.mock import patch, MagicMock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.order.tests.test_order import OrderSetupMixin


class PaymentAPITestCase(OrderSetupMixin, APITestCase):
    """TestCase to check that payment API works in expected way.

    Unittests used to mock false requests to LiqPay API.
    """

    def setUp(self):
        """Set up basic environment for test case."""
        self.product_setup()
        self.order_setup()

        # Reduce the log level to avoid messages like 'bad request'
        logger = logging.getLogger("django.request")
        self.previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

    def tearDown(self) -> None:
        """Reset the log level back to normal."""
        logger = logging.getLogger("django.request")
        logger.setLevel(self.previous_level)

    def assert_order_response_data(self, response_data):
        """Utility method to assert that order response contains necessary data."""
        self.assertIn("id", response_data)
        self.assertIn("orderNumber", response_data)
        self.assertIn("status", response_data)
        self.assertIn("firstName", response_data)
        self.assertIn("lastName", response_data)
        self.assertIn("phone", response_data)
        self.assertIn("isPaid", response_data)
        self.assertIn("cost", response_data)
        self.assertIn("items", response_data)
        self.assertIn("delivery", response_data)

    @patch("apps.payment.services.requests.post")
    def test_pay_action(self, mock_post):
        """Test that pay action works in expected way and returns payment url."""
        self.client.force_authenticate(user=self.admin_user)

        payment_mock = MagicMock()
        payment_mock.generate_new_url_for_pay.return_value = {"payment_url": "mock_payment_url"}

        mock_post.return_value.status_code = status.HTTP_200_OK
        mock_post.return_value.url = "mock_payment_url"

        with patch("apps.payment.services.Payment", return_value=payment_mock):
            url = reverse("order:orders-pay", kwargs={"pk": self.order.pk})
            response = self.client.post(url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, {"payment_url": "mock_payment_url"})

    @patch("apps.payment.services.requests.post")
    def test_failed_payment_action(self, mock_post):
        """
        Test payment action behaviour when the external payment service returns a 503 status.
        """
        self.client.force_authenticate(user=self.admin_user)

        payment_mock = MagicMock()

        mock_post.return_value.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        with patch("apps.payment.services.Payment", return_value=payment_mock):
            url = reverse("order:orders-pay", kwargs={"pk": self.order.pk})
            response = self.client.post(url)

            self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
            self.assertEqual(
                response.data, {"message": "Incorrect status code from response - 503"}
            )

    @patch("apps.payment.services.Payment.get_order_status_from_liqpay")
    def test_callback_endpoint_payment_success(self, mock_get_order_status):
        """
        Test the callback endpoint for handling successful payments.
        """
        self.client.force_authenticate(user=self.admin_user)

        # Mock the response from get_order_status_from_liqpay
        mock_get_order_status.return_value = {"result": "ok"}

        url = reverse("order:orders-callback")
        query_params = {"order_id": self.order.pk}
        url_with_params = (
            f"{url}?{'&'.join([f'{key}={value}' for key, value in query_params.items()])}"
        )

        response = self.client.get(url_with_params)
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["message"], "Payment was successful.")
        self.assert_order_response_data(response_data["order"])

        # Check if the order status and payment status are updated correctly
        self.order.refresh_from_db()
        self.assertTrue(self.order.is_paid)
        self.assertEqual(self.order.status, self.order.OrderStatusChoices.PROCESSING)

    @patch("apps.payment.services.Payment.get_order_status_from_liqpay")
    def test_callback_endpoint_payment_status_invalid(self, mock_get_order_status):
        """Test callback endpoint behaviour when payment wasn't done successfully."""
        self.client.force_authenticate(user=self.admin_user)

        # Mock the response from get_order_status_from_liqpay to return False
        mock_get_order_status.return_value = False

        url = reverse("order:orders-callback")
        query_params = {"order_id": self.order.pk}
        url_with_params = (
            f"{url}?{'&'.join([f'{key}={value}' for key, value in query_params.items()])}"
        )

        response = self.client.get(url_with_params)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Payment status not received or invalid.")
