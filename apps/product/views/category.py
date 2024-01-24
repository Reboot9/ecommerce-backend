"""
This module contains Category-related views.
"""
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from apps.base.pagination import PageNumberPagination
from apps.product.models import Category
from apps.product.serializers.category import CategorySerializer


class CategoryDetailView(generics.RetrieveAPIView):
    """
    API View for retrieving single category with its descendants.
    """

    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination

    def get_object(self):
        """
        Retrieving descendant categories based on the provided slugs.

        :return: queryset containing descendant categories
        """
        category_slug = self.kwargs.get("category_slug")
        subcategory_slug = self.kwargs.get("subcategory_slug")

        if category_slug:
            parent_category = get_object_or_404(Category, slug=category_slug)

            if subcategory_slug:
                descendant_category = get_object_or_404(
                    Category, parent=parent_category, slug=subcategory_slug
                )
                return descendant_category.subcategories.all()
            else:
                return parent_category.subcategories.all()
        else:
            # If no category slug is provided, return top-level categories
            return Category.objects.filter(level=0)

    def get(self, request, *args, **kwargs):
        """
        Get view for retrieving a category and its descendants.

        Retrieves the object, serializes it, and includes information about the requested
        category and its descendants in the response.

        :param request: The HTTP request.
        :param args: Variable-length argument list.
        :param kwargs: Arbitrary keyword arguments.
        :return: A Response object containing serialized data with information about the requested
        category and its descendants.
        If the category or its descendants are not found, returns an appropriate HTTP 404 response.
        """
        children_categories = self.get_object()
        serializer = self.get_serializer(children_categories, many=True)

        category_slug = self.kwargs.get("category_slug")
        subcategory_slug = self.kwargs.get("subcategory_slug")

        requested_category = None

        if subcategory_slug:
            requested_category = get_object_or_404(Category, slug=subcategory_slug)
        elif category_slug:
            requested_category = get_object_or_404(Category, slug=category_slug)

        response_data = {
            "category": CategorySerializer(requested_category).data
            if requested_category
            else None,
            "descendants": serializer.data,
        }

        return Response(response_data)
