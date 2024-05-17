"""
Test module for cart item related functionality.
"""
import logging
import uuid
from decimal import Decimal, ROUND_HALF_UP

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.cart.models import CartItem
from apps.product.models import Product
from apps.product.tests.test_product import ProductSetupMixin

User = get_user_model()


class CartItemTestCase(ProductSetupMixin, TestCase):
    """TestCase for general cart item operations and validation checks."""

    def setUp(self):
        """Set up basic environment for test case."""
        super().product_setup()

        self.cart = self.admin_user.carts.get(is_active=True)

        # Reduce the log level to avoid messages like 'bad request'
        logger = logging.getLogger("django.request")
        self.previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

    def tearDown(self) -> None:
        """Reset the log level back to normal."""
        logger = logging.getLogger("django.request")
        logger.setLevel(self.previous_level)

    def test_create_cart_item(self):
        """Test creation of cart item."""
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.cart, self.cart)
        self.assertEqual(cart_item.quantity, 2)

    def test_cost_calculation(self):
        """Test cart item cost calculated properly."""
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        expected_cost = (
            cart_item.quantity
            * cart_item.product.price
            * ((100 - cart_item.product.discount_percentage) / 100)
        )
        expected_cost = Decimal(expected_cost).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        self.assertEqual(cart_item.cost, expected_cost)

    def test_cart_item_default_quantity(self):
        """
        Test to verify the default quantity of the CartItem.
        """
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
        )
        self.assertEqual(cart_item.quantity, 1)

    def test_cart_item_positive_quantity_validator(self):
        """
        Test to verify the quantity validator of the CartItem.
        """
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=0,
        )
        with self.assertRaises(ValidationError):
            cart_item.full_clean()


class CartItemAPITestCase(ProductSetupMixin, APITestCase):
    """TestCase for cart item operations via the API."""

    def setUp(self):
        """Set up basic environment for test case."""
        super().product_setup()
        self.client.force_authenticate(user=self.admin_user)
        self.cart = self.admin_user.carts.get(is_active=True)

        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=4)

        self.product2 = Product.objects.create(
            name="Test Product 2",
            slug="test-product-2",
            price=100.00,
            product_code="TEST456",
            manufacturer=self.manufacturer,
            categories=self.lower_level_category,
            image="product/default.jpg",
        )

        # Reduce the log level to avoid messages like 'bad request'
        logger = logging.getLogger("django.request")
        self.previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

    def tearDown(self) -> None:
        """Reset the log level back to normal."""
        logger = logging.getLogger("django.request")
        logger.setLevel(self.previous_level)

    def assert_cart_item_response_data(self, response_data):
        """Utility method to assert that cart item response contains necessary data."""
        self.assertIn("id", response_data)
        self.assertIn("product", response_data)
        self.assertIn("quantity", response_data)

        # separate checks for product in response data
        product_data = response_data.get("product")
        self.assertIn("id", product_data)
        self.assertIn("name", product_data)
        self.assertIn("slug", product_data)
        self.assertIn("categories", product_data)
        self.assertIn("rating", product_data)
        self.assertIn("image", product_data)
        self.assertIn("price", product_data)

    def test_cart_item_list_obtain_authenticated(self):
        """Test cart item obtaining requires authentication."""
        url = reverse("cart:cart_items-list")

        response = self.client.get(url, format="json")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_cart_item_response_data(response_data[0])

    def test_cart_item_list_obtain_unauthenticated(self):
        """Test cart item is not possible without authentication."""
        self.client.logout()
        url = reverse("cart:cart_items-list")

        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_cart_item(self):
        """Test cart item retrieval via the API."""
        url = reverse("cart:cart_items-detail", kwargs={"pk": self.cart_item.id})
        response = self.client.get(url, format="json")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_cart_item_response_data(response_data)

    def test_retrieve_cart_item_stranger_user(self):
        """
        Test to verify retrieving a cart item that does not belong to the authenticated user.
        """
        other_user = User.objects.create_user(email="otheruser@test.com", password="password")
        other_cart = other_user.carts.get(is_active=True)
        other_cart_item = CartItem.objects.create(
            cart=other_cart,
            product=self.product,
            quantity=1,
        )
        url = reverse("cart:cart_items-detail", kwargs={"pk": other_cart_item.id})

        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_cart_item(self):
        """
        Test to verify creating a cart item via the API.
        """
        url = reverse("cart:cart_items-list")
        data = {
            "productID": self.product2.id,
            "quantity": 1,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 2)

    def test_create_cart_item_without_product_id(self):
        """
        Test that product id is required when creating cart item.
        """
        url = reverse("cart:cart_items-list")
        data = {
            "quantity": 1,
        }
        response = self.client.post(url, data, format="json")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_data["productID"], "productID is required when creating CartItem instance."
        )

    def test_create_cart_item_nonexistent_product(self):
        """Test to verify creating a cart item with a non-existent product via the API."""
        url = reverse("cart:cart_items-list")
        data = {
            "productID": uuid.uuid4(),
            "quantity": 1,
        }
        response = self.client.post(url, data, format="json")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid pk", str(response_data["productID"]))

    def test_update_quantity_for_exiting_cart_item(self):
        """
        Test that quantity is being updated if user creates cart item for existing product.
        """
        url = reverse("cart:cart_items-list")
        data = {
            "productID": self.product.id,
            "quantity": 2,
        }
        response = self.client.post(url, data, format="json")
        response_data = response.data
        expected_quantity = self.cart_item.quantity + data["quantity"]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["quantity"], expected_quantity)

    def test_update_cart_item(self):
        """Test updating cart item via the API."""
        url = reverse("cart:cart_items-detail", kwargs={"pk": self.cart_item.id})
        data = {
            "quantity": 3,
        }
        response = self.client.put(url, data, format="json")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_cart_item_response_data(response_data)

    def test_delete_cart_item(self):
        """
        Test to verify deleting a cart item via the API.
        """
        url = reverse("cart:cart_items-detail", kwargs={"pk": self.cart_item.pk})
        response = self.client.delete(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.count(), 0)
