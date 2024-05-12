"""
Test module for category related functionality.
"""
import logging

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from apps.product.models import Category
from apps.product.tests.test_product import ProductSetupMixin


class CategoryTestCase(ProductSetupMixin, TestCase):
    """
    TestCase for category related functionality, including creation, update and obtaining.
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

    def test_parent_child_relationship(self):
        """Check parent-child relationships."""
        self.assertEqual(self.top_level_category.parent, None)
        self.assertEqual(self.medium_level_category.parent, self.top_level_category)
        self.assertEqual(self.lower_level_category.parent, self.medium_level_category)

    def test_get_subcategories(self):
        """Test retrieving subcategories of a category."""
        subcategories = self.top_level_category.subcategories.all()

        self.assertEqual(len(subcategories), 1)
        self.assertIn(self.medium_level_category, subcategories)

    def test_update_category(self):
        """Test updating a category."""
        category = self.top_level_category
        category.name = "Updated Top Level Category"
        category.save()

        updated_category = Category.objects.get(pk=category.pk)

        self.assertEqual(updated_category.name, "Updated Top Level Category")

    def assert_response_data(self, response_data):
        """Utility method to assert the structure and content of the response data."""
        self.assertIn("id", response_data)
        self.assertIn("name", response_data)
        self.assertIn("slug", response_data)
        self.assertIn("level", response_data)
        self.assertIn("subcategories", response_data)

    def test_category_list_view(self):
        """
        Test case for the category list view API endpoint.
        """
        url = reverse("product:categories-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data

        # Check for pagination
        self.assertIn("count", response_data)
        self.assertIn("next", response_data)
        self.assertIn("previous", response_data)

        # Check if the results list contains one element
        self.assertEqual(len(response_data["results"]), 1)

        # Extract the first category
        category = response_data["results"][0]

        # Check if the category has the expected keys
        self.assert_response_data(category)

        lower_category = category["subcategories"][0]["subcategories"][0]

        # Check if there's lower category present in response
        self.assertEqual(lower_category["name"], self.lower_level_category.name)

    def test_category_descendants_list(self):
        """
        Test for retrieving a category based on the provided category slug.
        """
        url = reverse(
            "product:category-descendants-list",
            kwargs={"category_slug": self.top_level_category.slug},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data

        # Check if the response has expected keys
        self.assert_response_data(response_data)

    def test_category_descendants_with_invalid_category_slug(self):
        """
        Test that invalid category slug returns 404 error.
        """
        url = reverse(
            "product:category-descendants-list", kwargs={"category_slug": "invalid-slug"}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subcategory_descendants_list(self):
        """Test obtaining medium level category based on provided slugs."""
        url = reverse(
            "product:subcategory-descendants-list",
            kwargs={
                "category_slug": self.top_level_category.slug,
                "subcategory_slug": self.medium_level_category.slug,
            },
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data

        # Check if the response has expected keys
        self.assert_response_data(response_data)

    def test_subcategory_descendants_with_invalid_category_slug(self):
        """
        Test that invalid category slug returns 404 error for subcategory descendants view.
        """
        url = reverse(
            "product:subcategory-descendants-list",
            kwargs={
                "category_slug": "invalid-slug",
                "subcategory_slug": self.medium_level_category.slug,
            },
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subcategory_descendants_with_invalid_subcategory_slug(self):
        """
        Test that invalid subcategory slug returns 404 error for subcategory descendants view.
        """
        url = reverse(
            "product:subcategory-descendants-list",
            kwargs={
                "category_slug": self.top_level_category.slug,
                "subcategory_slug": "invalid-slug",
            },
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_product_list_by_category(self):
        """Test obtaining list of products filtered by categories."""
        url = reverse(
            "product:product-list-by-category",
            kwargs={
                "category_slug": self.top_level_category.slug,
                "subcategory_slug": self.medium_level_category.slug,
                "lower_category_slug": self.lower_level_category.slug,
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data

        # Check for pagination
        self.assertIn("count", response_data)
        self.assertIn("next", response_data)
        self.assertIn("previous", response_data)

        product_info = response_data["results"][0]

        # Check that product info for provided lower category is present
        self.assertIn("id", product_info)
        self.assertIn("slug", product_info)
        self.assertIn("name", product_info)
        self.assertIn("productCode", product_info)
        self.assertIn("price", product_info)
        self.assertIn("priceDiscount", product_info)
        self.assertEqual(product_info["categories"], self.lower_level_category.slug)

    def test_product_list_by_category_with_invalid_category_slug(self):
        """Test that invalid category slug returns 404 for product list by category endpoint."""
        url = reverse(
            "product:product-list-by-category",
            kwargs={
                "category_slug": "invalid-slug",
                "subcategory_slug": self.medium_level_category.slug,
                "lower_category_slug": self.lower_level_category.slug,
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_product_list_by_category_with_invalid_subcategory_slug(self):
        """Test that invalid subcategory slug returns 404 for product list by category endpoint."""
        url = reverse(
            "product:product-list-by-category",
            kwargs={
                "category_slug": self.top_level_category.slug,
                "subcategory_slug": "invalid-slug",
                "lower_category_slug": self.lower_level_category.slug,
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_product_list_by_category_with_invalid_lower_category_slug(self):
        """Test invalid lower category slug returns 404 for product list by category endpoint."""
        url = reverse(
            "product:product-list-by-category",
            kwargs={
                "category_slug": self.top_level_category.slug,
                "subcategory_slug": self.medium_level_category.slug,
                "lower_category_slug": "invalid-slug",
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
