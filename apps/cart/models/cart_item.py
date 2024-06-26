"""
This module defines the CartItem model for the cart app.
"""

import decimal
from decimal import Decimal, ROUND_HALF_UP

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseID, BaseDate
from apps.cart.models.cart import Cart
from apps.product.models import Product


class CartItem(BaseID, BaseDate):
    """Describes item from cart."""

    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(
        verbose_name=_("Item quantity"), default=1, validators=[MinValueValidator(1)]
    )

    class Meta:
        db_table = "cart_items"
        verbose_name = "Cart item"
        verbose_name_plural = "Cart items"

    def __str__(self) -> str:
        """
        This method is automatically called when you use the str() function.
        """
        return f"CartItem for {self.product} for {self.cart}, " f"cost - {self.cost}"

    @property
    def cost(self) -> decimal.Decimal:
        """Calculate the total cost of item in the cart."""
        cost = (
            self.quantity * self.product.price * ((100 - self.product.discount_percentage) / 100)
        )
        return Decimal(cost).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
