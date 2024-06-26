"""
This module defines the serializers for OrderItem model.
"""
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.base.serializers import BaseDateSerializer
from apps.order.models.order_item import OrderItem
from apps.product.models import Product
from apps.product.serializers.product import LiteProductSerializer


class OrderItemSerializer(BaseDateSerializer, serializers.ModelSerializer):
    """Serializer for OrderItem model."""

    # orderID = serializers.UUIDField(read_only=True, source="order_id")
    product = LiteProductSerializer(read_only=True)
    productID = serializers.UUIDField(required=True, write_only=True, source="product_id")
    # price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2,
    #                                  source="product.price")

    class Meta:
        model = OrderItem
        fields = ["id", "product", "productID", "quantity"]
        read_only_fields = [
            "id",
            "product",
        ]

    def update(self, instance, validated_data):
        """If object is being updated don't allow product to be changed."""
        validated_data.pop("product_id", None)
        return super().update(instance, validated_data)

    def create(self, validated_data):
        """Overriding create method to ensure productID is provided."""
        product_id = validated_data.pop("product_id")
        if product_id is None:
            raise serializers.ValidationError("Product ID is required.")
        product = get_object_or_404(Product, id=product_id)

        # Set price to product price if not provided
        validated_data["price"] = validated_data.get("price", product.price)

        # Default quantity to 1 if not provided
        validated_data["quantity"] = validated_data.get("quantity", 1)
        order_item = OrderItem.objects.create(
            **validated_data,
            product=product,
        )

        return order_item
