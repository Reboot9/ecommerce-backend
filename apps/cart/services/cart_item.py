"""
Module for working with CartItems.

This module provides functionality for creating CartItems.
"""
from uuid import UUID

from django.db.models import QuerySet

from apps.cart.models import CartItem
from apps.cart.services.cart import check_and_deactivate_empty_cart


def get_cart_item_detail(pk: UUID) -> QuerySet[CartItem]:
    """Return detailed data for a specific item in the Cart."""
    return CartItem.objects.select_related("cart", "product").filter(pk=pk)


def delete_cart_item(cartitem, cart):
    """Delete item from the cart."""
    cartitem.delete()
    check_and_deactivate_empty_cart(cart)
