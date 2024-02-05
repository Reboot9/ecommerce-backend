"""
Contains serializers for Category-related models.
"""
from typing import List

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

    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "level", "subcategories"]
        read_only_fields = ["id"]

    def get_subcategories(self, instance) -> List[dict]:
        """
        Retrieve and serialize the subcategories for a given category instance.

        :param instance: Category instance for which subcategories are to be retrieved.
        :return: list of serialized subcategories related to the provided category instance.
        """
        subcategories_qs = Category.objects.filter(parent_id=instance.id)
        serializer = CategoryListSerializer(subcategories_qs, many=True)
        return serializer.data
