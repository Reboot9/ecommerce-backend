"""
This module defines the serializers for OrderItem model.
"""
from rest_framework import serializers

from apps.base.serializers import BaseDateSerializer
from apps.order.models.order_item import OrderItem
from apps.product.serializers.product import LiteProductSerializer


class OrderItemSerializer(BaseDateSerializer, serializers.ModelSerializer):
    """Serializer for OrderItem model."""

    # orderID = serializers.UUIDField(read_only=True, source="order_id")
    # productID = serializers.UUIDField(required=True, source="product_id")
    product = LiteProductSerializer(read_only=True)
    price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "price", "quantity"]
        read_only_fields = [
            "id",
        ]
