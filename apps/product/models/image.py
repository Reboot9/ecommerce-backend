"""
Definition of the ProductImage model for the product app.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseDate, BaseID
from apps.product.models.product import Product


class ProductImage(BaseID, BaseDate):
    """Model representing an Additional Image of the Product."""

    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="product/%Y/%m/%d", verbose_name=_("Image path"))

    class Meta:
        db_table = "image"
        verbose_name = _("Additional Product Image")
        verbose_name_plural = _("Additional Product Images")
