"""
Module: delivery.py.

This module defines the serializers for delivery models.
"""
from rest_framework import serializers

from apps.base.serializers import BaseDateSerializer
from apps.order.models.delivery import Delivery


class DeliverySerializer(BaseDateSerializer, serializers.ModelSerializer):
    """Serializer for order."""

    street = serializers.CharField(required=False)
    house = serializers.CharField(required=False)
    flat = serializers.CharField(required=False)
    floor = serializers.IntegerField(required=False)
    entrance = serializers.IntegerField(required=False)
    department = serializers.CharField(required=False)
    time = serializers.DateField(required=False)
    declaration = serializers.CharField(required=False)

    class Meta:
        model = Delivery
        exclude = ("created_at", "updated_at")

        read_only_fields = ("id",)
