"""
Module: product.py.

This module defines the Product model for the product app.
"""
from decimal import Decimal, ROUND_HALF_UP

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseDate, BaseID
from apps.order.models.order import Order
from apps.product.models import Product


class OrderItem(BaseID, BaseDate):
    """Model representing an order item."""

    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=10,
        decimal_places=2,
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name=_("Item quantity"),
        default=1,
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="order_items",
    )
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    class Meta:
        db_table = "order_items"
        verbose_name = "Order item"
        verbose_name_plural = "Order items"

    def __str__(self) -> str:
        """This method is automatically called when you use the `str()` function.

        Or when the object needs to be represented as a string
        """
        return f"{self.product} from {self.order}"

    @property
    def order_item_cost(self) -> Decimal:
        """Calculate the total cost of item in the order."""
        cost = self.quantity * self.price * ((100 - self.discount_percentage) / 100)
        return Decimal(cost).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
