"""
Serializer for CartItem model.
"""
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.cart.models import CartItem
from apps.product.models import Product
from apps.product.serializers.product import LiteProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for goods in Cart."""

    # cartID = serializers.UUIDField(read_only=True, source="cart.id")
    # productID = serializers.UUIDField(required=False, source="product.id")
    product = LiteProductSerializer(read_only=True)
    discountPercentage = serializers.DecimalField(
        source="product.discount_percentage",
        max_digits=5,
        decimal_places=2,
        read_only=True,
    )
    price = serializers.DecimalField(
        source="product.price",
        max_digits=5,
        decimal_places=2,
        read_only=True,
    )
    cost = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "price", "discountPercentage", "cost"]
        read_only_fields = ["id", "price", "discountPercentage", "cost"]

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields.get("product").read_only = True
            self.fields.get("price").read_only = True

    def create(self, validated_data):
        """
        Create method for CartItem serializer.

        :param validated_data: validated data containing info about cart item.
        :return: newly created CartItem instance.
        """
        product_id = validated_data.get("product__id")
        product = get_object_or_404(Product, id=product_id)

        cart_item = CartItem.objects.create(
            product=product,
            cart=self.context["cart"],
            quantity=validated_data["quantity"],
        )

        return cart_item

    def update(self, instance, validated_data):
        """
        Update and return an existing CartItem instance, but only for changing the quantity field.

        :param instance: instance to update.
        :param validated_data: validated data containing info about cart item.
        :return: updated CartItem instance.
        """
        instance.quantity = validated_data.get("quantity", instance.quantity)
        instance.save()
        return instance
