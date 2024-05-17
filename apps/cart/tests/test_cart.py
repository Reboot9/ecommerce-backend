"""
Test module for cart related functionality.
"""
import logging
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.cart.models import Cart, CartItem
from apps.product.tests.test_product import ProductSetupMixin

User = get_user_model()


class CartTestCase(ProductSetupMixin, TestCase):
    """TestCase for general cart validation."""

    def setUp(self):
        """Set up basic environment for test case."""
        super().product_setup()

        self.cart1 = self.admin_user.carts.get(is_active=True)
        self.cart2 = Cart.objects.create(user=self.admin_user, is_active=False)

        self.cart1_item = CartItem.objects.create(
            cart=self.cart1, product=self.product, quantity=4
        )
        self.cart2_item = CartItem.objects.create(
            cart=self.cart2, product=self.product, quantity=100
        )

        # Reduce the log level to avoid messages like 'bad request'
        logger = logging.getLogger("django.request")
        self.previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

    def tearDown(self) -> None:
        """Reset the log level back to normal."""
        logger = logging.getLogger("django.request")
        logger.setLevel(self.previous_level)

    def test_unique_active_cart_for_user(self):
        """Test that a user can have only one active cart."""
        self.assertEqual(Cart.objects.filter(user=self.admin_user, is_active=True).count(), 1)

    def test_total_quantity(self):
        """Test calculation of total quantity of items in the cart."""
        self.assertEqual(self.cart1.total_quantity, 4)

    def test_total_price(self):
        """Test calculation of total price of items in the cart."""
        expected_price = (
            self.cart1_item.quantity
            * Decimal(self.cart1_item.product.price)
            * ((100 - Decimal(self.cart1_item.product.discount_percentage)) / 100)
        )

        self.assertEqual(self.cart1.total_price, expected_price)


class CartAPITestCase(ProductSetupMixin, APITestCase):
    """TestCase for Cart API to check that it works expected."""

    def setUp(self):
        """Set up basic environment for test case."""
        super().product_setup()

        self.cart = self.admin_user.carts.get(is_active=True)

        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=4)

        # Reduce the log level to avoid messages like 'bad request'
        logger = logging.getLogger("django.request")
        self.previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

    def tearDown(self) -> None:
        """Reset the log level back to normal."""
        logger = logging.getLogger("django.request")
        logger.setLevel(self.previous_level)

    def assert_cart_response_data(self, response_data):
        """Utility method to assert that cart response contains necessary data."""
        self.assertIn("id", response_data)
        self.assertIn("items", response_data)
        self.assertIn("totalQuantity", response_data)
        self.assertIn("totalPrice", response_data)

        items_data = response_data.get("items")[0]
        self.assertIn("quantity", items_data)
        self.assertIn("discountPercentage", items_data)
        self.assertIn("cost", items_data)

        # separate checks for product in response data
        product_data = items_data.get("product")
        self.assertIn("id", product_data)
        self.assertIn("name", product_data)
        self.assertIn("slug", product_data)
        self.assertIn("categories", product_data)
        self.assertIn("rating", product_data)
        self.assertIn("image", product_data)
        self.assertIn("price", product_data)

    def test_cart_list(self):
        """Test cart retrieval as list works."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("cart:carts-list")

        response = self.client.get(url)
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_cart_response_data(response_data[0])

    def test_cart_list_without_authentication(self):
        """Test user has to be authenticated to make requests."""
        url = reverse("cart:carts-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cart_retrieval(self):
        """Test cart retrieval as detail doesn't work."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("cart:carts-detail", kwargs={"pk": self.cart.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_cart_authenticated(self):
        """Test cart cannot be created via API."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("cart:carts-list")
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_destroy_cart_admin_user(self):
        """Test that admin can destroy cart."""
        self.client.force_authenticate(user=self.admin_user)

        url = reverse("cart:carts-detail", kwargs={"pk": self.cart.pk})
        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cart.objects.filter(pk=self.cart.pk, is_active=True).exists())

    def test_destroy_cart_non_admin(self):
        """Test that strangers can not destroy cart."""
        user = User.objects.create_user(email="someone@test.com", password="somepassword")
        self.client.force_authenticate(user=user)
        url = reverse("cart:carts-detail", kwargs={"pk": self.cart.pk})
        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
