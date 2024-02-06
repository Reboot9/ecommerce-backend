"""
Module for working with orders.

This module provides functionality for creating orders and associated order items.
"""
from django.db import transaction

from apps.order.models.order import Order
from apps.order.models.order_item import OrderItem
from apps.product.models import Product


@transaction.atomic
def create_order(items, validated_data):
    """Create an order."""
    order = Order.objects.create(**validated_data)
    get_order_items(order, items)
    return order


def get_order_items(order, items):
    """Get data to create order item."""
    for item in items:
        product_id = item["product_id"]
        quantity = item["quantity"]
        price = Product.objects.get(pk=product_id).price
        create_order_item(product_id, quantity, price, order)


def create_order_item(product_id, quantity, price, order):
    """Create order item for the given product, quantity, price, and associated order."""
    order_item = OrderItem.objects.create(
        order=order, price=price, quantity=quantity, product_id=product_id
    )
    return order_item
