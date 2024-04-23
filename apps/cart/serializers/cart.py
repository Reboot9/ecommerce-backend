"""
Module: cart.py.

This module defines the serializer for cart models.
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.cart.models import Cart
from apps.cart.serializers.cart_item import CartItemSerializer

User = get_user_model()


class CartSerializer(serializers.ModelSerializer):
    """Serializer that used for Carts."""

    totalQuantity = serializers.IntegerField(source="total_quantity", read_only=True)
    totalPrice = serializers.DecimalField(
        source="total_price",
        max_digits=5,
        decimal_places=2,
        read_only=True,
    )
    userID = serializers.UUIDField(source="user__pk", read_only=True)
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "userID", "items", "totalQuantity", "totalPrice"]
        read_only_fields = ["id", "userID", "totalQuantity", "totalPrice"]

    # def create(self, validated_data) -> Cart:
    #     """Create Cart with goods. Use the POST method."""
    #     items = validated_data.pop("items")
    #     user = self.context["user"]
    #     cart = create_or_update_cart(items, user)
    #     return cart
    #
    # def update(self, instance, validated_data) -> Cart:
    #     """Update item in Cart. Use the PATCH method."""
    #     items = validated_data.pop("items")
    #     return update_cart(instance, items)
