"""
Contains serializers for Manufacturer-related models.
"""

from rest_framework import serializers

from apps.product.models import Manufacturer


class ManufacturerSerializer(serializers.ModelSerializer):
    """
    Serializer for representation of a Manufacturer.
    """

    class Meta:
        model = Manufacturer
        exclude = ["created_at", "updated_at"]
        read_only_fields = ["id"]
