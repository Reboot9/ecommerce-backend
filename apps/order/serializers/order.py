"""
Module: order.py.

This module defines the serializers for order models.
"""
from decimal import Decimal

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.base.serializers import BaseDateSerializer
from apps.cart.models import Cart
from apps.order.models.order import Order
from apps.order.serializers.delivery import DeliverySerializer
from apps.order.serializers.order_item import OrderItemSerializer
from apps.order.services import create_order


class OrderSerializer(BaseDateSerializer, serializers.ModelSerializer):
    """Serializer for order."""

    items = OrderItemSerializer(
        many=True,
        required=False,
    )
    firstName = serializers.CharField(
        source="first_name",
        required=True,
    )
    lastName = serializers.CharField(source="last_name")
    email = serializers.EmailField(required=True, write_only=True)
    isPaid = serializers.BooleanField(source="is_paid", read_only=True, default=False)
    orderNumber = serializers.IntegerField(source="order_number", read_only=True)
    delivery = DeliverySerializer(required=False)
    comment = serializers.CharField(default="")
    cost = serializers.SerializerMethodField(
        read_only=True,
    )
    status = serializers.SerializerMethodField()
    # Additional field for cart_id
    cartID = serializers.UUIDField(write_only=True, required=False)

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
            "cost",
            "comment",
            "items",
            "delivery",
            "cartID",
        ]
        read_only_fields = ["id", "orderNumber", "status", "isPaid", "cost"]

    def validate(self, attrs):
        """Overriding validation to provide custom creation logic depending on params."""
        cart_id = attrs.get("cart_id")
        if cart_id and "items" in attrs:
            del attrs["items"]  # Remove "items" if cart_id is provided
        return attrs

    def create(self, validated_data) -> Order:
        """
        Create an Order instance based on provided validated data.

        Note, that there's two possible ways of creating an order: via items from cart when there's
        cartID in json data or by providing order items itself.
        """
        request = self.context.get("request")
        if request:
            cart_id = validated_data.pop("cartID", None)
            if cart_id:
                if not request.user.is_authenticated:
                    raise serializers.ValidationError(
                        "Only authenticated users can create orders via cart."
                    )
                cart = get_object_or_404(Cart, is_active=True, user=request.user, id=cart_id)
                validated_data["items"] = [
                    {"productID": item.product.id, "quantity": item.quantity}
                    for item in cart.items.all()
                ]

                if not validated_data["items"]:
                    raise serializers.ValidationError("Cannot create an order if cart is empty.")

        order_items = validated_data.pop("items", None)
        delivery = validated_data.pop("delivery", None)
        if order_items is None:
            raise serializers.ValidationError(
                "'items' or `cartID` is required when creating an instance."
            )
        if delivery is None:
            raise serializers.ValidationError("`delivery` is required when creating an instance.")

        order_instance = create_order(order_items, delivery, validated_data)

        return order_instance

    def get_cost(self, instance) -> Decimal:
        """
        Method to obtain total cost of order.

        :param instance: Order instance.
        :return: cost of the order
        """
        return instance.total_order_price

    def get_status(self, instance):
        """
        Method to obtain order status as display value.

        :param instance: Order instance.
        :return: display value of order status.
        """
        return instance.get_status_display()
