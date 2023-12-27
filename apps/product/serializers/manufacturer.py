"""
Module: image.py.

This module defines the ManufacturerSerializer for the Manufacturer model.
"""

from rest_framework import serializers

from apps.product.models import Manufacturer


class ManufacturerSerializer(serializers.ModelSerializer):
    """Class to operate with manufacturer."""

    class Meta:
        model = Manufacturer
        exclude = ["created_at", "updated_at"]
        read_only_fields = ["id"]
