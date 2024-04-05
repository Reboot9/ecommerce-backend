"""
Serializer for CartItem model.
"""
from rest_framework import serializers

from apps.cart.models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for goods in Cart."""

    cartID = serializers.UUIDField(read_only=True, source="cart_id")
    productID = serializers.UUIDField(read_only=True, source="product_id")
    discountPercentage = serializers.DecimalField(
        source="discount_percentage", max_digits=5, decimal_places=2, default=0, read_only=True
    )

    class Meta:
        model = CartItem
        fields = ["id", "cartID", "productID", "quantity", "price", "discountPercentage", "cost"]
        read_only_fields = ["id", "cartID", "price", "discountPercentage", "cost"]

    def update(self, instance, validated_data):
        """
        Update and return an existing CartItem instance, but only for changing the quantity field.
        """
        instance.quantity = validated_data.get("quantity", instance.quantity)
        instance.save()
        return instance
