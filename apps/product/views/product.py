"""
Module: views.py.

This module contains handler for the product app.
"""
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.base.pagination import PaginationCommon
from apps.product.filters.product import ProductFilter
from apps.product.mixins.category import CategoryMixin
from apps.product.models import Product
from apps.product.serializers.product import ProductListSerializer, ProductDetailSerializer


class ProductCategorytList(CategoryMixin, ListAPIView):
    """
    Returns a list of products, filtered by categories.

    - To filter by categories, provide the 'categories' parameter in the URL.
    - To sort by price or rating, use the 'ordering' parameter in the URL.
      - Example: /api/shop/category1/category2/category3/?ordering=price - by increase
      - Example: /api/shop/category1/category2/category3/?ordering=-price - by decrease
    - To filter by price or type of product, use the next URL
      - Example: /api/shop/category1/category2/category3/?min_price=1000&max_price=1500
    - To search, use the 'search' parameter in the URL
      - Example: /api/shop/category1/category2/category3/?search=brit
    - To paginate, use the 'page' parameter in the URL
      - Example: /api/shop/category1/category2/category3/?page=2&page_size=5
    """

    serializer_class = ProductListSerializer
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ["price", "rating"]
    search_fields = ["name", "manufacturer__trade_brand", "product_code"]
    pagination_class = PaginationCommon

    def get_queryset(self):
        """Different filters require different sets of queries."""
        category, subcategory, lower_category = self.get_categories()
        return (
            Product.objects.prefetch_related("product_characteristics", "types_product", "images")
            .select_related("manufacturer", "categories")
            .filter(categories=lower_category)
        )


class ProductDetail(CategoryMixin, RetrieveAPIView):
    """Returns one product."""

    serializer_class = ProductDetailSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "product_slug"

    def get_queryset(self):
        """Filters the queryset based on the product's unique slug."""
        category, subcategory, lower_category = self.get_categories()
        product_slug = self.kwargs.get("product_slug")
        return (
            Product.objects.prefetch_related("product_characteristics", "types_product", "images")
            .select_related("manufacturer", "categories")
            .filter(slug=product_slug, categories=lower_category)
        )


class ProductList(ListAPIView):
    """Returns a list of products sorted by creation date in descending order."""

    serializer_class = ProductListSerializer
    pagination_class = PaginationCommon
    queryset = (
        Product.objects.select_related("manufacturer", "categories")
        .prefetch_related("product_characteristics", "types_product", "images")
        .annotate(newest_first=F("created_at"))  # Add annotation for sorting
        .order_by("-newest_first")  # Order by creation date descending
        .all()
    )
