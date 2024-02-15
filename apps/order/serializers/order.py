"""
Module: order.py.

This module defines the serializers for order models.
"""
from rest_framework import serializers

from apps.base.serializers import BaseDateSerializer
from apps.order.models.order import Order
from apps.order.serializers.delivery import DeliverySerializer
from apps.order.serializers.order_item import OrderItemSerializer
from apps.order.services import create_order


class OrderSerializer(BaseDateSerializer, serializers.ModelSerializer):
    """Serializer for order."""

    items = OrderItemSerializer(many=True)
    firstName = serializers.CharField(source="first_name")
    lastName = serializers.CharField(source="last_name")
    isPaid = serializers.BooleanField(source="is_paid", default=False, required=False)
    orderNumber = serializers.IntegerField(source="order_number", read_only=True)
    delivery = DeliverySerializer()

    class Meta:
        model = Order
        fields = [
            "id",
            "orderNumber",
            "status",
            "firstName",
            "lastName",
            "phone",
            "email",
            "isPaid",
            "comment",
            "items",
            "delivery",
        ]
        read_only_fields = ["id", "orderNumber", "status", "isPaid"]

    def create(self, validated_data) -> Order:
        """Create order."""
        items = validated_data.pop("items")
        delivery = validated_data.pop("delivery")
        return create_order(items, delivery, validated_data)
