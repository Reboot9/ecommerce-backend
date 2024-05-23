"""
Test module for delivery related functionality.
"""
import logging

from django.test import TestCase

from apps.order.forms import DeliveryModelAdminForm
from apps.order.models.delivery import Delivery
from apps.order.serializers.delivery import DeliverySerializer


class DeliveryAdminTestCase(TestCase):
    """TestCase for Delivery model admin form validation."""

    def setUp(self):
        """Set up basic environment for test case."""
        self.form_data = {
            "option": Delivery.DeliveryOptionChoices.COURIER,
            "city": "Sample City",
            "street": "Sample Street",
            "house": "20B",
            "flat": "30/1",
            "floor": 3,
            "entrance": "Back Entrance",
            "department": "",
            "time": "2024-05-15",
            "declaration": "Sample Declaration",
        }

        # Reduce the log level to avoid messages like 'bad request'
        logger = logging.getLogger("django.request")
        self.previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

    def tearDown(self) -> None:
        """Reset the log level back to normal."""
        logger = logging.getLogger("django.request")
        logger.setLevel(self.previous_level)

    def test_clean_with_courier_option_valid(self):
        """Test clean method with valid data for COURIER option."""
        form = DeliveryModelAdminForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_clean_with_courier_option_missing_required_fields(self):
        """Test clean method with COURIER option and missing required fields."""
        self.form_data.update({"street": "", "entrance": "", "time": None})
        form = DeliveryModelAdminForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("street", form.errors)
        self.assertIn("entrance", form.errors)
        self.assertIn("time", form.errors)

    def test_clean_with_courier_option_missing_house_and_flat(self):
        """Test clean method with COURIER option missing both house and flat."""
        self.form_data.update({"house": "", "flat": ""})
        form = DeliveryModelAdminForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)

    def test_clean_with_delivery_option_valid(self):
        """Test clean method with valid data for DELIVERY option."""
        self.form_data.update(
            {
                "option": Delivery.DeliveryOptionChoices.DELIVERY,
                "department": "Sales",
                "street": "",
                "entrance": "",
                "time": None,
                "house": "",
                "flat": "",
            }
        )
        form = DeliveryModelAdminForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_clean_with_delivery_option_missing_department(self):
        """Test clean method with DELIVERY option missing department."""
        self.form_data.update(
            {
                "option": Delivery.DeliveryOptionChoices.DELIVERY,
                "department": "",
            }
        )
        form = DeliveryModelAdminForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("department", form.errors)


class DeliverySerializerTestCase(TestCase):
    """TestCase for Delivery serializer."""

    def test_validate_option_required(self):
        """Test that option field is required when creating an instance."""
        data = {
            "city": "test city",
        }
        serializer = DeliverySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("option", serializer.errors)

    def test_validate_courier_required_fields(self):
        """Test that required fields are validated for courier option."""
        data = {
            "option": Delivery.DeliveryOptionChoices.COURIER,
            "street": "",
            "entrance": "",
            "time": None,
        }
        serializer = DeliverySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("street", serializer.errors)
        self.assertIn("entrance", serializer.errors)
        self.assertIn("time", serializer.errors)

    def test_validate_courier_house_or_flat_required(self):
        """Test that either house or flat is required for courier delivery."""
        data = {
            "city": "test city",
            "option": Delivery.DeliveryOptionChoices.COURIER,
            "street": "Sample Street",
            "entrance": "Back Entrance",
            "time": "2024-05-15",
        }
        serializer = DeliverySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(serializer.errors["non_field_errors"][0].code, "invalid")

    def test_validate_delivery_required_department(self):
        """Test that department is required for delivery option."""
        data = {
            "option": Delivery.DeliveryOptionChoices.DELIVERY,
            "city": "test city",
        }
        serializer = DeliverySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("department", serializer.errors)

    def test_validate_optional_fields(self):
        """Test that optional fields can be left blank."""
        data = {
            "option": Delivery.DeliveryOptionChoices.DELIVERY,
            "city": "test city",
            "department": "Sales",
        }
        serializer = DeliverySerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_validate_valid_data(self):
        """Test that serializer validates valid data."""
        data = {
            "option": Delivery.DeliveryOptionChoices.COURIER,
            "city": "test city",
            "street": "Sample Street",
            "entrance": "Back Entrance",
            "time": "2024-05-15",
            "house": "20B",
            "flat": "30/1",
            "floor": 3,
            "department": "Sales",
        }
        serializer = DeliverySerializer(data=data)

        self.assertTrue(serializer.is_valid())
