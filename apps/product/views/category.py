"""
This module contains Category-related views.
"""
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.base.mixins import CachedListView
from apps.product.models import Category
from apps.product.serializers.category import CategoryDetailSerializer, CategoryListSerializer

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class CategoryDetailView(generics.RetrieveAPIView):
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
            f"category_detail_{category_slug}_{subcategory_slug}"
            if subcategory_slug
            else f"category_detail_{category_slug}"
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

    def retrieve(self, request, *args, **kwargs) -> Response:
        """
        Retrieve a single category by their slug.

        :param request: The HTTP request object.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: details of the requested Category.
        """
        cache_key = self.get_cache_key()

        # Try to get data from cache
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        # if not in cache, fetch from the database
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # set data in cache for future requests
        cache.set(cache_key, data, timeout=CACHE_TTL)

        return Response(data)


class CategoryListView(CachedListView, generics.ListAPIView):
    """
    API View for retrieving list of categories.
    """

    serializer_class = CategoryListSerializer
    queryset = Category.objects.prefetch_related("subcategories").filter(parent=None)
    pagination_class = PageNumberPagination
    page_size = 100

    def get_cache_key(self) -> str:
        """
        Method to get cache key for list of categories.

        :return: cache key for the provided category
        """
        return "category_list"
