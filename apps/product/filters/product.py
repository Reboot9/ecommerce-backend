"""
This module filters the Product model for the product app.
"""
from django_filters import rest_framework as filters

from apps.product.models import Product


class ProductFilter(filters.FilterSet):
    """The class for product filtering."""

    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    manufacturer = filters.CharFilter(field_name="manufacturer__trade_brand", lookup_expr="iexact")
    type_characteristic = filters.CharFilter(
        field_name="types_product__type_characteristic", lookup_expr="iexact"
    )

    class Meta:
        model = Product
        fields = ["min_price", "max_price", "manufacturer", "type_characteristic"]
