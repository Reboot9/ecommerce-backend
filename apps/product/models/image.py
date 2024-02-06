"""
Module: image.py.

This module defines the Image model for the product app.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseDate, BaseID
from apps.product.models.product import Product


class Image(BaseID, BaseDate):
    """Model representing an image ."""

    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="product/%Y/%m/%d", verbose_name=_("Image path"))

    class Meta:
        db_table = "image"
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
