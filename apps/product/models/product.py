"""
Module: product.py.

This module defines the Product model for the product app.
"""
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseDate, BaseID
from apps.product.models.category import Category
from apps.product.models.manufacturer import Manufacturer


class Product(BaseID, BaseDate):
    """Model representing a product."""

    class ProductStockChoices(models.TextChoices):
        """Enum for product status."""

        IN_STOCK = "I", _("In stock")
        NOT_AVAILABLE = "N", _("Not available")
        WITHDRAWN_FROM_SALE = "W", _("Withdrawn from sale")
        AWAITING = "A", _("Awaiting")

    name = models.CharField(max_length=256, verbose_name=_("Name"))
    slug = models.SlugField(max_length=256, unique=True)
    description_short = models.CharField(
        max_length=256, null=True, blank=True, verbose_name=_("Short description")
    )
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    rating = models.DecimalField(
        verbose_name=_("Rating"),
        max_digits=3,  # 4.99 / 5
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0, message="Rating cannot be less than 0"),
            MaxValueValidator(5, message="Rating cannot be more than 5"),
        ],
        help_text=_("Enter a rating between 0 and 5."),
    )
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[
            MinValueValidator(0, message=_("Discount percentage cannot be less than 0.")),
            MaxValueValidator(100, message=_("Discount percentage cannot be greater than 100.")),
        ],
    )
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("This field allows empty value"),
    )
    product_code = models.CharField(max_length=256, verbose_name=_("Product code"), unique=True)
    stock = models.CharField(
        verbose_name=_("Stock"),
        max_length=1,
        choices=ProductStockChoices.choices,
        default=ProductStockChoices.IN_STOCK,
    )
    manufacturer = models.ForeignKey(
        to=Manufacturer,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Manufacturer"),
    )
    categories = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name="product_categories",
        verbose_name=_("Categories"),
    )
    image = models.ImageField(upload_to="product/%Y/%m/%d", verbose_name=_("Image path"))

    class Meta:
        ordering = ["-created_at"]
        db_table = "products"
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        constraints = [
            models.CheckConstraint(
                name="price_is_positive",
                check=Q(price__gte=0) | Q(price__isnull=True),
                violation_error_message=_("Price must be positive or empty."),
            ),
            models.CheckConstraint(
                name="rating_from_0_to_5",
                check=Q(rating__gte=0) & Q(rating__lte=5),
                violation_error_message=_("Rating must has to equal from 0 to 5."),
            ),
        ]

    def __str__(self) -> str:
        """This method is automatically called when you use the `str()` function.

        Or when the object needs to be represented as a string
        """
        return f"{self.name}-{self.product_code}"

    @property
    def price_discount(self):
        """Method for calculating promotional price."""
        if self.price:
            return self.price * ((100 - self.discount_percentage) / 100)
        else:
            return None

    def delete(self, *args, **kwargs):
        """TODO: describe this method when the app warehouse will be ready.

        Prohibit removal if the product is in stock or write a signal.
        """
        pass


class ProductCharacteristics(BaseID, BaseDate):
    """Model representing a product characteristic.

    For example: weight, feed class.
    """

    name = models.CharField(max_length=256, verbose_name=_("Product characteristic"), unique=True)
    categories = models.ManyToManyField(
        to=Category,
        db_table="category characteristic m2m",
        related_name="characteristic_categories",
        blank=True,
    )
    product = models.ManyToManyField(
        to=Product,
        db_table="product characteristic m2m",
        related_name="product_characteristics",
        blank=True,
    )

    class Meta:
        db_table = "product characteristic"
        verbose_name = _("Product characteristic")
        verbose_name_plural = _("Product characteristics")

    def __str__(self) -> str:
        """This method is automatically called when you use the `str()` function.

        Or when the object needs to be represented as a string
        """
        return f"{self.name}"


class TypeProductCharacteristics(BaseID, BaseDate):
    """Model representing a type of product characteristic.

    For example: premium, 1.5kg
    feed class - premium, weight - 1.5kg.
    """

    name = models.CharField(
        max_length=256, verbose_name=_("Type of product characteristic"), unique=True
    )
    product = models.ManyToManyField(
        to=Product, db_table="type product m2m", related_name="types_product", blank=True
    )
    product_characteristics = models.ForeignKey(
        to=ProductCharacteristics, on_delete=models.CASCADE, related_name="characteristic_product"
    )

    class Meta:
        db_table = "type characteristics"
        verbose_name = _("Type of product characteristics")
        verbose_name_plural = _("Types of product characteristics")

    def __str__(self) -> str:
        """This method is automatically called when you use the `str()` function.

        Or when the object needs to be represented as a string.
        """
        return f"{self.name}"
