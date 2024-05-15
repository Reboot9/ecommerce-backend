"""
Test module for order related functionality.
"""
import json
import logging
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.cart.models import Cart, CartItem
from apps.order.models.order import Order
from apps.order.models.order_item import OrderItem
from apps.product.models import Product
from apps.product.tests.test_product import ProductSetupMixin

User = get_user_model()


class OrderSetupMixin(ProductSetupMixin):
    """
    Mixin for setting up test data related to orders.

    This mixin provides a setup method for creating necessary objects related to orders
    for testing purposes.
    """

    def order_setup(self):
        """
        Set up necessary objects related to orders for testing.
        """
        self.order = Order.objects.create(
            status=Order.OrderStatusChoices.NEW,
            first_name="John",
            last_name="Doe",
            phone="+38(050)111-11-11",
            email=self.admin_user.email,
            order_number=12345,
        )

        self.order1 = Order.objects.create(
            order_number="45678",
            status=Order.OrderStatusChoices.EXECUTED,
            email="something@test.com",
            first_name="John",
            last_name="Doe",
            phone="+38(050)111-11-11",
        )


class OrderTestCase(OrderSetupMixin, TestCase):
    """
    TestCase for general order operations, related to calculation methods and validation.
    """

    def setUp(self):
        """
        Set up basic environment for test case.
        """
        super().product_setup()
        super().order_setup()

        self.product1 = Product.objects.create(
            name="Second product",
            slug="second-product",
            description_short="Short description",
            description="This is a test product description.",
            rating=3,
            price=1.00,
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

    def test_total_order_price_calculation(self):
        """
        Test the calculation of the total order price.
        """
        order = self.order
        self.assertEqual(order.total_order_price, Decimal("0"))

        # Add items to the order and test the calculation again
        order_item1 = OrderItem.objects.create(  # noqa: F841
            order=order,
            product=self.product,
            quantity=2,
            price=Decimal("10.00"),
            discount_percentage=0,
        )
        order_item2 = OrderItem.objects.create(  # noqa: F841
            order=order,
            product=self.product1,
            quantity=1,
            price=Decimal("20.00"),
            discount_percentage=10,
        )

        expected_total_price = (2 * Decimal("10.00")) + (1 * Decimal("20.00") * Decimal("0.9"))
        self.assertEqual(order.total_order_price, expected_total_price)

    def test_invalid_order_number(self):
        """
        Test that creating an order with a duplicate order number raises a validation error.
        """
        Order.objects.create(order_number="1001", status="N", is_paid=False)

        # Attempt to create another order with the same order number
        with self.assertRaises(IntegrityError):
            Order.objects.create(order_number="1001", status="N", is_paid=False)


class OrderAPITestCase(OrderSetupMixin, APITestCase):
    """TestCase to check that order API works in expected way."""

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
        self.assertTrue(Order.objects.filter(id=response_data["id"]).exists())

    def test_order_creation_with_and_without_auth(self):
        """Test order creation via API."""
        self.test_create_order(with_auth=True)
        self.test_create_order(with_auth=False)

    def test_create_order(self, with_auth=True):
        """Test order creation via API."""
        if not with_auth:
            self.client.logout()

        data = {
            "firstName": "testname",
            "lastName": "testlastname",
            "phone": "+38(050)111-11-11",
            "email": "valid@email.com",
            "items": [{"productID": self.product.id, "quantity": 2}],
            "delivery": {"city": "test", "option": "D", "department": "test"},
        }

        url = reverse("order:orders-list")
        response = self.client.post(url, data=data, format="json")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assert_order_response_data(response_data)

    def test_order_creation_via_cart_with_and_without_auth(self):
        """
        Test the order creation process through the cart both with and without user authentication.
        """
        self.test_order_create_via_cart(with_auth=True)
        self.test_order_create_via_cart(with_auth=False)

    def test_order_create_via_cart(self, with_auth=True):
        """
        Test the order creation process through the cart with an optional authentication parameter.

        Depending on the `with_auth` parameter, this test will simulate the order creation process
        either as an authenticated user or as an anonymous user.
        """
        if not with_auth:
            self.client.logout()
        else:
            self.client.force_authenticate(user=self.admin_user)

        user_cart = self.admin_user.carts.filter(is_active=True).first()

        # Check if an active cart exists for the user
        if user_cart is None:
            # If no active cart exists, create a new one
            user_cart = Cart.objects.create(user=self.admin_user)

        # add cart item to user's cart so cart will be valid for request.
        cart_item = CartItem.objects.create(cart=user_cart, product=self.product, quantity=1)  # noqa: F841
        data = {
            "firstName": "testname",
            "lastName": "testlastname",
            "phone": "+38(050)111-11-11",
            "email": "valid@email.com",
            "cartID": user_cart.id,
            "delivery": {"city": "test", "option": "D", "department": "test"},
        }

        url = reverse("order:orders-list")
        response = self.client.post(url, data=data, format="json")
        response_data = response.data

        if with_auth:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assert_order_response_data(response_data)
        else:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(
                response_data["detail"], "Only authenticated users can create orders via cart."
            )

    def test_create_order_missing_delivery(self):
        """
        Test that delivery param is required when creating order.
        """
        data = {
            "firstName": "testname",
            "lastName": "testlastname",
            "phone": "+38(050)111-11-11",
            "email": "valid@email.com",
            "items": [{"productID": self.product.id, "quantity": 2}],
        }

        url = reverse("order:orders-list")
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content.decode())[0],
            "`delivery` is required when creating an instance.",
        )

    def test_create_order_missing_items_and_cart(self):
        """
        Test neither cartID or items required to create an order.
        """
        data = {
            "firstName": "testname",
            "lastName": "testlastname",
            "phone": "+38(050)111-11-11",
            "email": "valid@email.com",
            "delivery": {"city": "test", "option": "D", "department": "test"},
        }

        url = reverse("order:orders-list")
        response = self.client.post(url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content.decode())[0],
            "'items' or `cartID` is required when creating an instance.",
        )

    def test_order_obtain_authenticated_user(self):
        """Test that order owner an admin can obtain the order."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("order:orders-detail", kwargs={"pk": self.order.pk})

        response = self.client.get(url, format="json")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response_data["id"], str(self.order.id))
        self.assertEqual(response_data["orderNumber"], self.order.order_number)
        self.assertEqual(response_data["status"], self.order.get_status_display())
        self.assertEqual(response_data["firstName"], self.order.first_name)
        self.assertEqual(response_data["lastName"], self.order.last_name)
        self.assertEqual(response_data["phone"], self.order.phone)
        self.assertEqual(response_data["isPaid"], self.order.is_paid)
        self.assertEqual(response_data["items"], list(self.order.items.all()))
        self.assertEqual(response_data["delivery"], self.order.delivery)

    def test_order_obtain_stranger_order(self):
        """Test that stranger cannot obtain other's orders."""
        user = User.objects.create_user(email="test@test.com", password="testpassword")
        self.client.force_authenticate(user=user)
        url = reverse("order:orders-detail", kwargs={"pk": self.order1.pk})
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_obtain_unauthenticated_user(self):
        """Test that authentication is required to obtain orders."""
        self.client.logout()
        url = reverse("order:orders-detail", kwargs={"pk": self.order.pk})

        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_patch_as_admin(self):
        """Test that admin can patch an order."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("order:orders-detail", kwargs={"pk": self.order.pk})
        data = {"firstName": "test"}
        response = self.client.patch(url, data=data, format="json")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assert_order_response_data(response_data)
        self.order.refresh_from_db()
        self.assertEqual(self.order.first_name, "test")

    def test_order_patch_as_non_admin(self):
        """Test that other users cannot patch orders."""
        self.client.logout()
        user = User.objects.create_user(email="something@test.com", password="userpassword")
        self.client.force_authenticate(user=user)

        data = {"firstName": "test"}
        url = reverse("order:orders-detail", kwargs={"pk": self.order1.pk})
        response = self.client.patch(url, data=data, format="json")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response_data["detail"], "You do not have permission to perform this action."
        )
