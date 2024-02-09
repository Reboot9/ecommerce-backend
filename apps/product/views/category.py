"""
This module contains Category-related views.
"""
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from apps.base.mixins import CachedListView, CachedRetrieveView
from apps.base.pagination import PaginationCommon
from apps.product.models import Category
from apps.product.serializers.category import CategoryDetailSerializer, CategoryListSerializer

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class CategoryDetailView(CachedRetrieveView, generics.RetrieveAPIView):
    """
    API View for retrieving single category with its descendants.
    """

    serializer_class = CategoryDetailSerializer

    def get_cache_key(self) -> str:
        """
        Method to get cache key for a specific category.

        :return: cache key for the provided category
        """
        category_slug = self.kwargs.get("category_slug")
        subcategory_slug = self.kwargs.get("subcategory_slug")
        return (
            f"category_detail_{category_slug}_{subcategory_slug}:"
            f"{hash(frozenset(self.request.query_params.items()))}"
            if subcategory_slug
            else f"category_detail_{category_slug}:"
            f"{hash(frozenset(self.request.query_params.items()))}"
        )

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


class CategoryListView(CachedListView, generics.ListAPIView):
    """
    API View for retrieving list of categories.
    """

    serializer_class = CategoryListSerializer
    queryset = Category.objects.prefetch_related("subcategories").filter(parent=None)
    pagination_class = PaginationCommon

    def get_cache_key(self) -> str:
        """
        Method to get cache key for list of categories.

        :return: cache key for the provided category
        """
        return f"category_list:{hash(frozenset(self.request.query_params.items()))}"
