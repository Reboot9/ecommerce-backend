"""
This module contains Category-related views.
"""
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.product.models import Category
from apps.product.serializers.category import CategoryDetailSerializer, CategoryListSerializer


class CategoryDetailView(generics.RetrieveAPIView):
    """
    API View for retrieving single category with its descendants.
    """

    serializer_class = CategoryDetailSerializer

    def get_object(self):
        """
        Retrieving descendant categories based on the provided slugs.

        :return: queryset containing descendant categories
        """
        category_slug = self.kwargs.get("category_slug")
        subcategory_slug = self.kwargs.get("subcategory_slug")

        if category_slug:
            parent_category = get_object_or_404(Category, slug=category_slug, level=0)

            if subcategory_slug:
                descendant_category = get_object_or_404(
                    Category, parent=parent_category, slug=subcategory_slug, level=1
                )
                return descendant_category
            else:
                return parent_category
        else:
            # If no category slug is provided, return 404
            return Response(status=status.HTTP_404_NOT_FOUND)


class CategoryListView(generics.ListAPIView):
    """
    API View for retrieving list of categories.
    """

    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()
    pagination_class = PageNumberPagination
    page_size = 100
