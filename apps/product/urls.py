"""
Module: urls.py.

This module contains urls for the product app.
"""

from django.urls import path

from apps.product.views.manufacturer import ManufacturerListView
from apps.product.views.product import ProductDetailView, ProductCategoryListView, ProductListView
from apps.product.views.category import CategoryListView, CategoryDetailView

app_name = "product"

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list"),
    path("manufacturers/", ManufacturerListView.as_view(), name="manufacturer-list"),
    path("", CategoryListView.as_view(), name="categories-list"),
    path(
        "<slug:category_slug>/",
        CategoryDetailView.as_view(),
        name="category-descendants-list",
    ),
    path(
        "<slug:category_slug>/<slug:subcategory_slug>/",
        CategoryDetailView.as_view(),
        name="subcategory-descendants-list",
    ),
    path(
        "<slug:category_slug>/<slug:subcategory_slug>/<slug:lower_category_slug>/",
        ProductCategoryListView.as_view(),
        name="product-list-by-category",
    ),
    path(
        "<slug:category_slug>/<slug:subcategory_slug>/<slug:lower_category_slug>"
        "/<slug:product_slug>/",
        ProductDetailView.as_view(),
        name="product-detail-by-category",
    ),
]
