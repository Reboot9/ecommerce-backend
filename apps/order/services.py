"""
Functions responsible for creating orders and associated order items.
"""
from django.db import transaction
from django.shortcuts import get_object_or_404

from apps.order.models.delivery import Delivery
from apps.order.models.order import Order
from apps.order.models.order_item import OrderItem
from apps.product.models import Product


@transaction.atomic
def create_order(items: dict, delivery: dict, validated_data: dict) -> Order:
    """Create an order with delivery and order items."""
    delivery_instance = Delivery.objects.create(**delivery)
    order = Order.objects.create(delivery=delivery_instance, **validated_data)
    get_order_items(order, items)
    return order


def get_order_items(order: Order, items: dict):
    """Create order items for the given order."""
    for item in items:
        product_id = item.get("product_id")
        if product_id is None:
            raise ValueError("Product ID is missing.")
        # quantity = item.get("quantity", 1)
        # price = Product.objects.get(pk=product_id).price
        # discount_percentage = Product.objects.get(pk=product_id).discount_percentage
        product = get_object_or_404(Product, pk=product_id)
        create_order_item(order, product, item.get("quantity", 1))


def create_order_item(order: Order, product: Product, quantity: int) -> None:
    """Create an order item for the given product and quantity."""
    price = product.price
    discount_percentage = product.discount_percentage

    OrderItem.objects.create(
        order=order,
        product=product,
        price=price,
        quantity=quantity,
        discount_percentage=discount_percentage,
    )
    # return order_item
