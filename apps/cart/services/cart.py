"""
This module provides functionality for creating carts and associated cart items.
"""

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404

from apps.cart.models import CartItem, Cart
from apps.product.models import Product

User = get_user_model()


@transaction.atomic
def update_cart(instance, items):
    """Update the quantities of items in the cart."""
    for item in items:
        product_id = item["product_id"]
        quantity = item["quantity"]
        instance.items.filter(product_id=product_id).update(quantity=quantity)
    return instance


# def create_or_add_cart_item(
#     cart: Cart, product_id: UUID, price: decimal, discount_percentage: decimal
# ) -> CartItem:
#     """Create a new items or update items and return it."""
#     cart_item, created = CartItem.objects.get_or_create(
#         cart=cart,
#         product_id=product_id,
#     )
#     if not created:
#         cart_item.update()
#     return cart_item


# def get_product_for_cart(cart: Cart, items: list[dict]):
#     """Get product, its quantity, price and return it."""
#     for item in items:
#         product_id = item["product_id"]
#         price = get_object_or_404(Product, pk=product_id).price
#         discount_percentage = get_object_or_404(Product, pk=product_id).discount_percentage
#         create_or_add_cart_item(cart, product_id, price, discount_percentage)


@transaction.atomic
def create_or_update_cart(items: list[dict], user: User) -> Cart:
    """Create or update a cart for the specified user with the provided items."""
    cart, _ = Cart.objects.get_or_create(user=user, is_active=True)
    for item in items:
        product_id = item["product_id"]
        product = get_object_or_404(Product, pk=product_id)  # noqa: F841
        CartItem.objects.filter(cart=cart, product_id=product_id).update(
            quantity=F("quantity") + 1
        )
    return cart


def deactivate_empty_cart(cart: Cart):
    """Make the cart inactive if it's empty."""
    if cart.items.count() == 0:
        cart.is_active = False
        cart.save()
