"""
Module: manufacturer.py.

This module defines the Manufacturer model for the product app.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseDate, BaseID


class Manufacturer(BaseID, BaseDate):
    """Model representing a manufacturer."""

    trade_brand = models.CharField(max_length=256, verbose_name=_("Brand"))
    country = models.CharField(max_length=256, verbose_name=_("Country"))
    country_brand_registration = models.CharField(
        max_length=256, verbose_name=_("Country of brand registration")
    )

    class Meta:
        db_table = "manufacturer"
        verbose_name = _("Manufacturer")
        verbose_name_plural = _("Manufacturers")

    def __str__(self) -> str:
        """This method is automatically called when you use the `str()` function.

        Or when the object needs to be represented as a string
        """
        return f"{self.trade_brand}"
