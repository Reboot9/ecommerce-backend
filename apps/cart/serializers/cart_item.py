"""
Serializer for CartItem model.
"""
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.cart.models import CartItem
from apps.product.models import Product
from apps.product.serializers.product import LiteProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for goods in Cart."""

    # cartID = serializers.UUIDField(read_only=True, source="cart.id")
    # productID = serializers.UUIDField(required=False, source="product.id")
    productID = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), required=False, write_only=True
    )
    product = LiteProductSerializer(read_only=True)
    discountPercentage = serializers.DecimalField(
        source="product.discount_percentage",
        max_digits=5,
        decimal_places=2,
        read_only=True,
    )
    # price = serializers.DecimalField(
    #     source="product.price",
    #     max_digits=5,
    #     decimal_places=2,
    #     read_only=True,
    # )
    cost = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = CartItem
        fields = ["id", "product", "productID", "quantity", "discountPercentage", "cost"]
        read_only_fields = ["id", "discountPercentage", "cost"]

    def __init__(self, *args, **kwargs):
        """If object is being updated don't allow contact to be changed."""
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields.get("product").read_only = True
            # self.fields.get("price").read_only = True

    def create(self, validated_data):
        """
        Create method for CartItem serializer.

        :param validated_data: validated data containing info about cart item.
        :return: newly created CartItem instance.
        """
        cart = self.context["cart"]

        # Extract productID from validated data
        product_id = validated_data.get("productID")
        quantity = validated_data.get("quantity", 1)

        if not product_id:
            raise ValidationError("productID is required when creating CartItem instance.")

        # Check if a cart item with the same product already exists in the cart
        existing_cart_item = CartItem.objects.filter(cart=cart, product=product_id).first()

        if existing_cart_item:
            # If the item already exists, update its quantity
            existing_cart_item.quantity += quantity
            existing_cart_item.save()

            return existing_cart_item
        else:
            # If the item does not exist, create a new cart item
            cart_item = CartItem.objects.create(product=product_id, cart=cart, quantity=quantity)

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
