"""
This module contains Category-related views.
"""
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from apps.base.pagination import PageNumberPagination
from apps.product.models import Category
from apps.product.serializers.category import CategorySerializer


class CategoryListView(generics.ListAPIView):
    """
    API View for retrieving list of categories.
    """

    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """
        Retrieving categories and subcategories based on the provided slugs.

        :return: queryset containing descendant categories
        """
        category_slug = self.kwargs.get("category_slug")
        subcategory_slug = self.kwargs.get("subcategory_slug")

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)

            if subcategory_slug:
                subcategory = get_object_or_404(Category, parent=category, slug=subcategory_slug)
                return subcategory.subcategories.all()
            else:
                return category.subcategories.all()
        else:
            # If no category slug is provided, return top-level categories
            return Category.objects.filter(level=0)

    def list(self, request, *args, **kwargs):
        """
        List view for retrieving a category and its descendants.

        Retrieves the queryset, serializes it, and includes information about the requested
        category and its descendants in the response.

        :param request: The HTTP request.
        :param args: Variable-length argument list.
        :param kwargs: Arbitrary keyword arguments.
        :return: A Response object containing serialized data with information about the requested
        category and its descendants.
        If the category or its descendants are not found, returns an appropriate HTTP 404 response.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        category_slug = self.kwargs.get("category_slug")
        subcategory_slug = self.kwargs.get("subcategory_slug")

        category = None

        if subcategory_slug:
            category = get_object_or_404(Category, slug=subcategory_slug)
        elif category_slug:
            category = get_object_or_404(Category, slug=category_slug)

        response_data = {
            "category": CategorySerializer(category).data if category else None,
            "descendants": serializer.data,
        }

        return Response(response_data)
