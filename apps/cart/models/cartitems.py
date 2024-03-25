"""
This module defines the CartItem model for the cart app.
"""

import decimal
from decimal import Decimal, ROUND_HALF_UP

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseID, BaseDate
from apps.cart.models.cart import Cart
from apps.product.models import Product


class CartItem(BaseID, BaseDate):
    """Describes item from cart."""

    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(verbose_name=_("Item quantity"), default=1)
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=10,
        decimal_places=2,
    )
    discount_percentage = models.DecimalField(
        # TODO add a condition in constraint for product, it must be less than or equal to 100
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    class Meta:
        db_table = "cart_items"
        verbose_name = "Cart item"
        verbose_name_plural = "Cart items"

    def __str__(self) -> str:
        """This method is automatically called when you use the str() function.

        Or when the object needs to be represented as a string
        """
        return f"{self.product}, price - {self.price}"

    @property
    def cost(self) -> decimal.Decimal:
        """Calculate the total cost of item in the cart."""
        # TODO DO I NEED TO ADD discount_percentage, cost METHOD AND TOTAL PRICE TO ORDER
        #  for admin???
        cost = self.quantity * self.price * ((100 - self.discount_percentage) / 100)
        return Decimal(cost).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
