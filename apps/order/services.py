"""
Module for working with orders.

This module provides functionality for creating orders and associated order items.
"""
import decimal
from typing import Collection
from uuid import UUID

from django.db import transaction

from apps.order.models.delivery import Delivery
from apps.order.models.order import Order
from apps.order.models.order_item import OrderItem
from apps.product.models import Product


@transaction.atomic
def create_order(
    items: Collection[dict], delivery: Collection[dict], validated_data: dict
) -> Order:
    """Create an order."""
    delivery_item = Delivery.objects.create(**delivery)
    order = Order.objects.create(**validated_data, delivery=delivery_item)
    get_order_items(order, items)
    return order


def get_order_items(order: Order, items: Collection[dict]):
    """Get data to create order item."""
    for item in items:
        product_id = item["product_id"]
        quantity = item.get("quantity", 1)
        price = Product.objects.get(pk=product_id).price
        create_order_item(product_id, quantity, price, order)


def create_order_item(product_id: UUID, quantity: int, price: decimal, order: Order) -> OrderItem:
    """Create order item for the given product, quantity, price, and associated order."""
    order_item = OrderItem.objects.create(
        order=order, price=price, quantity=quantity, product_id=product_id
    )
    return order_item
