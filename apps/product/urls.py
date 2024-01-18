"""
Module: urls.py.

This module contains urls for the product app.
"""

from django.urls import path

from apps.product.views.manufacturer import ManufacturerList
from apps.product.views.product import ProductList, ProductDetail

app_name = "product"

urlpatterns = [
    path("products/", ManufacturerList.as_view(), name="manufacturer-list"),
    path("products/<uuid:categories>/", ProductList.as_view(), name="product-list-categories"),
    path(
        "products/<uuid:categories>/<slug:product_slug>/",
        ProductDetail.as_view(),
        name="product-detail",
    ),
]
