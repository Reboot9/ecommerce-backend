"""
Module: cart.py.

This module defines the serializer for cart models.
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.cart.models import Cart
from apps.cart.serializers.cartitem import CartItemSerializer

User = get_user_model()


class CartSerializer(serializers.ModelSerializer):
    """Serializer that used for Carts."""

    totalQuantity = serializers.IntegerField(source="total_quantity", read_only=True)
    totalPrice = serializers.DecimalField(
        source="total_price",
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )
    userID = serializers.IntegerField(source="user_id", read_only=True)
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "userID", "items", "totalQuantity", "totalPrice"]
        read_only_fields = ["id", "userID", "totalQuantity", "totalPrice"]
