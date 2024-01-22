"""
Module: views.py.

This module contains handler for the product app.
"""
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.base.pagination import PaginationCommon
from apps.product.filters.product import ProductFilter
from apps.product.models import Product, Category
from apps.product.serializers.product import ProductListSerializer, ProductDetailSerializer


class ProductList(ListAPIView):
    """
    Returns a list of products, filtered by categories.

    - To filter by categories, provide the 'categories' parameter in the URL.
    - To sort by price or rating, use the 'ordering' parameter in the URL.
      - Example: /products/some_category/?ordering=price - by increase
      - Example: /products/some_category/?ordering=-price - by decrease
    - To filter by price or type of product, use the next URL
      - Example: /product/4ef6debc-d407-4de0-929c-0412a15ad61d/?min_price=1000&max_price=1500
    - To search, use the 'search' parameter in the URL
      - Example: /product/4ef6debc-d407-4de0-929c-0412a15ad61d/?search=brit
    - To paginate, use the 'page' parameter in the URL
      - Example: /product/4ef6debc-d407-4de0-929c-0412a15ad61d/?page=2&page_size=5
    """

    serializer_class = ProductListSerializer
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ["price", "rating"]
    search_fields = ["name", "manufacturer__trade_brand", "product_code"]
    pagination_class = PaginationCommon

    def get_queryset(self):
        """Different filters require different sets of queries."""
        category_slug = self.kwargs.get("category_slug")
        subcategory_slug = self.kwargs.get("subcategory_slug")
        lower_category_slug = self.kwargs.get("lower_category_slug")

        category = get_object_or_404(Category, slug=category_slug)
        subcategory = get_object_or_404(Category, parent=category, slug=subcategory_slug)
        lower_category = get_object_or_404(Category, parent=subcategory, slug=lower_category_slug)
        return (
            Product.objects.prefetch_related("product_characteristics", "types_product", "images")
            .select_related("manufacturer", "categories")
            .filter(categories=lower_category)
        )


class ProductDetail(RetrieveAPIView):
    """Returns one product."""

    serializer_class = ProductDetailSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "product_slug"

    def get_queryset(self):
        """Filters the queryset based on the product's unique slug."""
        product_slug = self.kwargs.get("product_slug")
        return (
            Product.objects.prefetch_related("product_characteristics", "types_product", "images")
            .select_related("manufacturer", "categories")
            .filter(slug=product_slug)
        )
