"""
Module: cart.py.

This module defines the Cart model for the cart app.
"""
from decimal import Decimal, ROUND_HALF_UP

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import (
    DecimalField,
    ExpressionWrapper,
    PositiveIntegerField,
    Q,
    Sum,
    UniqueConstraint,
    F,
)

from apps.base.models import BaseID, BaseDate

User = get_user_model()


class Cart(BaseID, BaseDate):
    """Describe cart."""

    # this field has a one to many connection because cart becomes inactive after deleting
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="carts")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "carts"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        constraints = [
            UniqueConstraint(
                fields=["user", "is_active"],
                condition=Q(is_active=True),
                name="unique_active_cart_for_user",
            )
        ]

    @property
    def total_quantity(self):
        """Count the total number of items in the cart."""
        return (
            self.items.aggregate(
                total_quantity=ExpressionWrapper(
                    Sum("quantity"), output_field=PositiveIntegerField()
                )
            )["total_quantity"]
            or 0
        )

    @property
    def total_price(self):
        """Calculate the total cost of items in the cart."""
        total_price = self.items.aggregate(
            total_price=Sum(
                ExpressionWrapper(
                    F("quantity") * F("price") * ((100 - F("discount_percentage")) / 100),
                    output_field=DecimalField(),
                )
            )
        )["total_price"] or Decimal("0")
        return Decimal(total_price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def __str__(self) -> str:
        """This method is automatically called when you use the str() function.

        Or when the object needs to be represented as a string
        """
        return (
            f"Cart for {self.user}, Created: {self.created_at.date()} "
            f"Is Active: {self.is_active}"
        )
