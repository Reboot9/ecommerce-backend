"""
Module: delivery.py.

This module defines the Delivery model for the order app.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseDate, BaseID


class Delivery(BaseID, BaseDate):
    """Model representing a delivery."""

    city = models.CharField(
        max_length=250,
        verbose_name=_("City"),
    )
    option = models.CharField(
        max_length=250,
        verbose_name=_("Delivery option"),
    )
    street = models.CharField(
        max_length=250,
        verbose_name=_("Street"),
        null=True,
        blank=True,
    )
    house = models.CharField(
        max_length=50,
        verbose_name=_("House"),
        null=True,
        blank=True,
    )
    flat = models.CharField(
        max_length=20,
        verbose_name=_("Flat"),
        null=True,
        blank=True,
    )
    floor = models.SmallIntegerField(
        verbose_name=_("Floor"),
        null=True,
        blank=True,
    )
    entrance = models.PositiveSmallIntegerField(
        verbose_name=_("Entrance"),
        null=True,
        blank=True,
    )
    department = models.CharField(
        max_length=250,
        verbose_name=_("Department"),
        null=True,
        blank=True,
    )
    time = models.DateField(
        verbose_name=_("Delivery time"),
        null=True,
        blank=True,
    )
    declaration = models.CharField(  # discuss with frontend how to fill it
        max_length=250,
        verbose_name=_("Declaration"),
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "deliveries"
        verbose_name = "Delivery"
        verbose_name_plural = "Deliveries"

    def __str__(self):
        """This method is automatically called when you use the str() function.

        Or when the object needs to be represented as a string
        """
        if self.option == "Delivery":  # ??????????????? discuss with frontend
            return (
                f"{self.city}, {self.option}, Department: {self.department}, "
                f"Declaration: {self.declaration}"
            )
        else:
            return (
                f"{self.city}, {self.option}, Street: {self.street}, House: {self.house}, "
                f"Flat: {self.flat}, Floor: {self.floor}, Entrance: {self.entrance}, "
                f"Delivery time: {self.time},"
            )
