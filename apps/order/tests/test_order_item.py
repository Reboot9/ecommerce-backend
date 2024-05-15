"""
Tests for order items related functionality.
"""
import logging
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.order.models.order_item import OrderItem
from apps.order.tests.test_order import OrderSetupMixin

User = get_user_model()


class OrderItemTestCase(OrderSetupMixin, TestCase):
    """Test Order item operations, such as creation, validation and calculation methods."""

    def setUp(self):
        """
        Set up basic environment for test case.
        """
        super().product_setup()
        super().order_setup()

        # Reduce the log level to avoid messages like 'bad request'
        logger = logging.getLogger("django.request")
        self.previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

    def tearDown(self) -> None:
        """Reset the log level back to normal."""
        logger = logging.getLogger("django.request")
        logger.setLevel(self.previous_level)

    def test_order_item_creation(self):
        """Test order item creation."""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=Decimal("10.00"),
            quantity=2,
            discount_percentage=10,
        )
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.price, Decimal("10.00"))
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.discount_percentage, Decimal("10.00"))

    def test_order_item_cost(self):
        """Test cost for order item calculated properly."""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=Decimal("10.00"),
            quantity=2,
            discount_percentage=10,
        )
        expected_cost = 2 * Decimal("10.00") * (Decimal("1") - Decimal("0.1"))
        self.assertEqual(order_item.order_item_cost, expected_cost)

    def test_order_item_invalid_quantity(self):
        """Test order item validation on invalid quantity."""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=Decimal("10.00"),
            quantity=0,  # Invalid quantity
            discount_percentage=10,
        )
        with self.assertRaises(ValidationError):
            order_item.clean()  # Should raise ValidationError

    def test_order_item_negative_discount(self):
        """Test order item validation on negative discount."""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=Decimal("10.00"),
            quantity=1,
            discount_percentage=-10,  # Invalid discount
        )
        with self.assertRaises(ValidationError):
            order_item.clean()

    def test_order_item_excessive_discount(self):
        """Test order item validation on excessive discount."""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=Decimal("10.00"),
            quantity=1,
            discount_percentage=110,  # Invalid discount
        )
        with self.assertRaises(ValidationError):
            order_item.clean()


class OrderItemAPITestCase(OrderSetupMixin, APITestCase):
    """Test Order item API."""

    def setUp(self):
        """
        Set up basic environment for test case.
        """
        super().product_setup()
        super().order_setup()
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=Decimal("10.00"),
            quantity=1,
            discount_percentage=10,
        )

        # Reduce the log level to avoid messages like 'bad request'
        logger = logging.getLogger("django.request")
        self.previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

    def tearDown(self) -> None:
        """Reset the log level back to normal."""
        logger = logging.getLogger("django.request")
        logger.setLevel(self.previous_level)

    def assert_order_item_response_data(self, response_data):
        """Utility method to assert that order item response contains necessary data."""
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

    def test_order_item_list_authenticated(self):
        """Test order item list obtain."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("order:order-items-list", kwargs={"order_id": self.order.id})

        response = self.client.get(url, format="json")
        response_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assert_order_item_response_data(response_data[0])

    def test_list_order_items_unauthenticated(self):
        """Test login required to obtain order items list."""
        self.client.logout()
        url = reverse("order:order-items-list", kwargs={"order_id": self.order.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_order_item_authenticated(self):
        """Test retrieve of order item as admin and order owner."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse(
            "order:order-items-detail",
            kwargs={"order_id": self.order.pk, "pk": self.order_item.pk},
        )
        response = self.client.get(url, format="json")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assert_order_item_response_data(response_data)

    def test_retrieve_order_item_unauthenticated(self):
        """Test retrieving order item as stranger doesn't work."""
        url = reverse(
            "order:order-items-detail",
            kwargs={"order_id": self.order.pk, "pk": self.order_item.pk},
        )
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_item(self, with_auth=True):
        """
        Test the order item creation process with and without authentication parameter.

        Depending on the `with_auth` parameter, this test will simulate the order item
        creation process either as an authenticated user or as an anonymous user.
        """
        if with_auth:
            self.client.force_authenticate(user=self.admin_user)
        else:
            self.client.logout()

        data = {"productID": self.product.id, "quantity": 3}
        url = reverse("order:order-items-list", kwargs={"order_id": self.order.id})

        response = self.client.post(url, data=data, format="json")
        response_data = response.data

        if with_auth:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assert_order_item_response_data(response_data)
        else:
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(
                response_data["detail"], "Authentication credentials were not provided."
            )

    def test_create_order_item_with_and_without_auth(self):
        """Test order item creation cases both with and without authentication."""
        self.test_create_order_item(with_auth=True)
        self.test_create_order_item(with_auth=False)

    def test_create_order_item_stranger_user(self):
        """Test that stranger cannot create an order item."""
        user = User.objects.create_user(email="someone@mail.com", password="somepassword")
        self.client.force_authenticate(user=user)

        data = {"productID": self.product.id, "quantity": 3}
        url = reverse("order:order-items-list", kwargs={"order_id": self.order.id})

        response = self.client.post(url, data=data, format="json")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response_data["detail"], "You do not have permission to perform this action."
        )

    def test_update_order_item_as_admin(self):
        """Test that only admin can update order items."""
        self.client.force_authenticate(user=self.admin_user)

        url = reverse(
            "order:order-items-detail",
            kwargs={"order_id": self.order.pk, "pk": self.order_item.pk},
        )
        data = {"quantity": 2}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order_item.refresh_from_db()
        self.assertEqual(self.order_item.quantity, 2)

    def test_update_order_item_as_non_admin(self):
        """Test that updating order item as stranger would return an error."""
        user = User.objects.create_user(email="something@test.com", password="userpassword")
        self.client.force_authenticate(user=user)

        data = {"quantity": 2}
        url = reverse(
            "order:order-items-detail",
            kwargs={"order_id": self.order.pk, "pk": self.order_item.pk},
        )
        response = self.client.patch(url, data=data, format="json")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response_data["detail"], "You do not have permission to perform this action."
        )
