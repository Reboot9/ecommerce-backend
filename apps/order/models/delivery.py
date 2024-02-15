"""
Module: delivery.py.

This module defines the Delivery model for the order app.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseDate, BaseID


class Delivery(BaseID, BaseDate):
    """Model representing a delivery."""

    class DeliveryOptionChoices(models.TextChoices):
        DELIVERY = "D", _("Delivery")
        COURIER = "С", _("Сourier")

    option = models.CharField(
        verbose_name=_("Delivery option"),
        choices=DeliveryOptionChoices.choices,
        default=DeliveryOptionChoices.COURIER,
    )
    city = models.CharField(
        max_length=250,
        verbose_name=_("City"),
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
    declaration = models.CharField(  # TODO discuss with frontend how to fill it
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
        if self.get_option_display() == "Delivery":
            return (
                f"{self.city}, {self.get_option_display()}, Department: {self.department}, "
                f"Declaration: {self.declaration}"
            )
        else:
            return (
                f"{self.city}, {self.get_option_display()}, Street: {self.street}, "
                f"House: {self.house}, Flat: {self.flat}, Floor: {self.floor}, "
                f"Entrance: {self.entrance}, Delivery time: {self.time},"
            )
