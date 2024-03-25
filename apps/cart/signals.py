"""
Module: cart signals.

This module contains Django signals related to the Cart models.
"""
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.cart.models import Cart, CartItem
from apps.cart.services.cart import deactivate_cart
from apps.order.models.order import Order
from apps.product.models import Product

User = get_user_model()


@receiver(post_save, sender=Product)
def update_cart_prices(sender, instance, **kwargs):
    """Update prices in the active carts when a product price changes."""
    cart_is_active = Cart.objects.filter(is_active=True)
    for cart in cart_is_active:
        CartItem.objects.filter(cart=cart, product=instance).update(price=instance.price)


@receiver(post_save, sender=Order)
def delete_cart_after_order(sender, instance, created, **kwargs):
    """Make the cart inactive after creating an order."""
    if created:
        try:
            user = User.objects.get(email=instance.email)
            cart = Cart.objects.get(user=user, is_active=True)
            deactivate_cart(cart)
        except ObjectDoesNotExist:
            pass  # Cart or user not found, this is possible in two cases if the user is not
            # registered or the order was created through the admin panel without a cart
