"""
Module: image.py.

This module defines the ImageSerializer for the Image model.
"""

from rest_framework import serializers

from apps.product.models import Image


class ImageSerializer(serializers.ModelSerializer):
    """Class to operate with Image."""

    class Meta:
        model = Image
        exclude = ["created_at", "updated_at"]
        read_only_fields = ["id"]
