"""
Module: views.py.

This module contains handler for the product app.
"""
from rest_framework import viewsets

from apps.product.models import Product
from apps.product.serializers.product import ProductListSerializer, ProductDetailSerializer


class ProductSet(viewsets.ModelViewSet):
    """Handler for operation with product."""

    http_method_names = ["get"]
    lookup_field = "slug"

    def get_serializer_class(self):
        """Different endpoints require different serializers."""
        if self.action == "list":
            return ProductListSerializer
        if self.action in {"retrieve"}:
            return ProductDetailSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        """Different serializers require different querysets."""
        if self.action == "list":
            return Product.objects.all()
        if self.action in ["retrieve"]:
            return (
                Product.objects.prefetch_related(
                    "product_characteristics", "types_product", "images"
                )
                .select_related("manufacturer", "categories")
                .filter(slug=self.kwargs["slug"])
            )
        return super().get_queryset()
