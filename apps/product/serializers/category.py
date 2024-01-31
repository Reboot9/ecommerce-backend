"""
Contains serializers for Category-related models.
"""
from rest_framework import serializers

from apps.product.models import Category


class SubcategorySerializer(serializers.ModelSerializer):
    """
    Serializer for representing a subcategory in a simplified manner.
    """

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "level"]
        read_only_fields = ["id", "parent"]


class CategoryDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed representation of a Category, including subcategories.
    """

    parent = SubcategorySerializer()
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent", "level", "subcategories"]
        depth = 1
        read_only_fields = ["id", "parent"]


class CategoryListSerializer(serializers.ModelSerializer):
    """
    Serializer for simplified representation of a Category without subcategories.
    """

    parentId = serializers.UUIDField(source="parent.id", read_only=True, allow_null=True)
    parentSlug = serializers.SlugField(source="parent.slug", read_only=True, allow_null=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "level", "parentId", "parentSlug"]
        read_only_fields = ["id"]
