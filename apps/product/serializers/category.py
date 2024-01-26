"""
Contains serializers for Category-related models.
"""
from rest_framework import serializers

from apps.product.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """

    parentSlug = serializers.SlugField(source="parent.slug", read_only=True, allow_null=True)

    class Meta:
        model = Category
        fields = ["id", "slug", "name", "level", "parentSlug"]
        read_only_fields = ["id"]
