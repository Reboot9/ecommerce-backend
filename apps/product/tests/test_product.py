"""
Test module for product related functionality.
"""
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.product.models import Product, Manufacturer, Category

User = get_user_model()


class ProductSetupMixin:
    """
    Mixin for setting up test data related to products.

    This mixin provides a setup method for creating necessary objects related to products
    for testing purposes.
    """

    def product_setup(self):
        """
        Set up necessary objects related to products for testing purposes.

        This method creates instances of necessary objects such as categories, products,
        and manufacturers that are required for testing product-related functionalities.
        """
        # Create a user for admin login
        self.admin_user = User.objects.create_user(
            email="admin@t.com", password="admin-password", is_staff=True
        )

        self.manufacturer = Manufacturer.objects.create(
            trade_brand="Test Brand",
            country="Test Country",
            country_brand_registration="Test Brand Registration",
        )

        self.category = Category.objects.create(name="Test Category Name", slug="test-category")
        self.subcategory = Category.objects.create(
            name="Test Subcategory", slug="test-subcategory", parent=self.category
        )
        self.lower_category = Category.objects.create(
            name="Test Lower Category", slug="test-lower-category", parent=self.subcategory
        )

        # Create sample product data
        self.product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            description_short="Short description",
            description="This is a test product description.",
            rating=4.75,
            discount_percentage=10,
            price=100.00,
            product_code="TEST123",
            manufacturer=self.manufacturer,
            categories=self.lower_category,
            image="product/default.jpg",
        )


class ProductTestCase(ProductSetupMixin, TestCase):
    """
    TestCase for general product tests, including creation and validation.
    """

    def setUp(self):
        """
        Set up basic environment for test case.
        """
        super().product_setup()

    def test_create_product(self):
        """
        Test product creation.
        """
        product = Product.objects.get(name="Test Product")
        self.assertEqual(product.description_short, "Short description")
        self.assertEqual(product.description, "This is a test product description.")
        self.assertEqual(product.rating, 4.75)
        self.assertEqual(product.discount_percentage, 10)
        self.assertEqual(product.price, 100.00)
        self.assertEqual(product.product_code, "TEST123")
        self.assertEqual(product.manufacturer.trade_brand, "Test Brand")
        self.assertEqual(product.categories.name, "Test Lower Category")
        self.assertEqual(product.image, "product/default.jpg")

    def test_rating_validation(self):
        """
        Test rating validation.
        """
        instance = self.product
        instance.rating = 10

        with self.assertRaises(ValidationError) as context:
            instance.full_clean()
        self.assertEqual(context.exception.messages[0], "Rating cannot be more than 5")

    def test_price_is_positive(self):
        """
        Test positive price constraint.
        """
        with self.assertRaises(ValidationError) as context:
            instance = self.product
            instance.price = -1
            instance.full_clean()
        self.assertEqual(context.exception.messages[0], "Price must be positive or empty.")

    def test_discount_percentage_validation(self):
        """
        Test discount percentage validation.
        """
        with self.assertRaises(ValidationError) as context:
            instance = self.product
            instance.discount_percentage = 101
            instance.full_clean()
        self.assertEqual(
            context.exception.messages[0], "Discount percentage cannot be greater than 100."
        )

    def test_stock_choices(self):
        """
        Test stock is in valid choices list.
        """
        with self.assertRaises(ValidationError) as context:
            instance = self.product
            instance.stock = "x"
            instance.full_clean()
        self.assertEqual(context.exception.messages[0], "Value 'x' is not a valid choice.")

    def test_price_discount(self):
        """
        Test price_discount method calculation.
        """
        instance = self.product
        self.assertAlmostEqual(instance.price_discount, 90.00, places=2)

        # test that product's price without discount equals to it's price
        instance.discount_percentage = 0
        self.assertEqual(instance.price_discount, instance.price)


class ProductAPITestCase(ProductSetupMixin, APITestCase):
    """
    TestCase for API endpoints.
    """

    def setUp(self):
        """
        Set up basic environment for test case.
        """
        super().product_setup()

    def test_product_list(self):
        """
        Test the product list endpoint.
        """
        url = reverse("product:product-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test Product", str(response.data))

        # Check for pagination
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)

        expected_keys = [
            "id",
            "slug",
            "name",
            "productCode",
            "descriptionShort",
            "price",
            "priceDiscount",
            "categories",
            "discountPercentage",
            "typesProduct",
            "image",
            "rating",
        ]
        for product_data in response.data["results"]:
            for key in expected_keys:
                self.assertIn(key, product_data)

    def test_product_detail(self):
        """
        Test product detail endpoint.
        """
        url = reverse(
            "product:product-detail-by-category",
            kwargs={
                "category_slug": self.category.slug,
                "subcategory_slug": self.subcategory.slug,
                "lower_category_slug": self.lower_category.slug,
                "product_slug": self.product.slug,
            },
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)
        self.assertEqual(response.data["slug"], self.product.slug)
        self.assertEqual(response.data["productCode"], self.product.product_code)
        self.assertEqual(response.data["price"], f"{self.product.price:.2f}")
        self.assertEqual(response.data["priceDiscount"], f"{self.product.price_discount:.2f}")
        self.assertEqual(response.data["categories"], self.lower_category.slug)
        self.assertEqual(response.data["manufacturer"]["id"], str(self.manufacturer.id))

    def test_product_category_list(self):
        """Test the product list by category endpoint."""
        url = reverse(
            "product:product-list-by-category",
            kwargs={
                "category_slug": self.category.slug,
                "subcategory_slug": self.subcategory.slug,
                "lower_category_slug": self.lower_category.slug,
            },
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for pagination
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)

        self.assertIn("name", response.data["results"][0])
