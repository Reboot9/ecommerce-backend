"""
Test module for manufacturer related functionality.
"""
import logging

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from apps.product.models import Manufacturer
from apps.product.serializers.manufacturer import ManufacturerSerializer
from apps.product.tests.test_product import ProductSetupMixin


class ManufacturerTestCase(ProductSetupMixin, TestCase):
    """
    TestCase for manufacturer related functionality.
    """

    def setUp(self):
        """
        Set up basic environment for test case.
        """
        super().product_setup()

        # Reduce the log level to avoid messages like 'bad request'
        logger = logging.getLogger("django.request")
        self.previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)

    def tearDown(self) -> None:
        """Reset the log level back to normal."""
        logger = logging.getLogger("django.request")
        logger.setLevel(self.previous_level)

    def test_get_manufacturer_list(self):
        """
        Test to verify that the ManufacturerListView returns a list of manufacturers.
        """
        url = reverse("product:manufacturer-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Manufacturer.objects.count())

    def test_get_manufacturer_list_content(self):
        """
        Test to verify the content of the ManufacturerListView response.
        """
        url = reverse("product:manufacturer-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Manufacturer.objects.count())

        # Check if the response data matches the serialized data
        serialized_data = ManufacturerSerializer(Manufacturer.objects.all(), many=True).data
        self.assertEqual(response.data, serialized_data)

    def test_get_manufacturer_list_empty(self):
        """
        Test that ManufacturerListView returns an empty list when there are no manufacturers.
        """
        Manufacturer.objects.all().delete()
        url = reverse("product:manufacturer-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
