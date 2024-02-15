"""
Module: order_item.py.

This module defines the serializers for orderitem models.
"""
from rest_framework import serializers

from apps.base.serializers import BaseDateSerializer
from apps.order.models.order_item import OrderItem


class OrderItemSerializer(BaseDateSerializer, serializers.ModelSerializer):
    """Serializer for order_item."""

    orderID = serializers.UUIDField(read_only=True, source="order_id")
    productID = serializers.UUIDField(required=True, source="product_id")
    price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = ["id", "orderID", "productID", "price", "quantity"]
        read_only_fields = ["id", "orderID", "productID"]
