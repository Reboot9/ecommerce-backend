"""
Module: serializers.py.

This module contains serializers for handling data serialization in the base app.
"""

from rest_framework import serializers


class BaseDateSerializer(serializers.ModelSerializer):
    """Serializer to converts snake_case into camelCase for date fields."""

    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)
