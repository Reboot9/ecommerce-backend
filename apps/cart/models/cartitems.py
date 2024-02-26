"""
Module: cartitems.py.

This module defines the Cartitem model for the cart app.
"""

import decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseID, BaseDate
from apps.cart.models.cart import Cart
from apps.product.models import Product


class CartItem(BaseID, BaseDate):
    """Describe item of cart."""

    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(verbose_name=_("Item quantity"), default=1)
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=10,
        decimal_places=2,
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
        return self.quantity * self.price
