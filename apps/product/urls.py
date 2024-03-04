"""
Module: urls.py.

This module contains urls for the product app.
"""

from django.urls import path

from apps.product.views.manufacturer import ManufacturerList
from apps.product.views.product import ProductDetail, ProductCategorytList, ProductList
from apps.product.views.category import CategoryListView, CategoryDetailView

app_name = "product"

urlpatterns = [
    path("products/", ProductList.as_view(), name="product-list"),
    path("manufacturers/", ManufacturerList.as_view(), name="manufacturer-list"),
    path("shop/", CategoryListView.as_view(), name="categories-list"),
    path(
        "shop/<slug:category_slug>/",
        CategoryDetailView.as_view(),
        name="category-descendants-list",
    ),
    path(
        "shop/<slug:category_slug>/<slug:subcategory_slug>/",
        CategoryDetailView.as_view(),
        name="subcategory-descendants-list",
    ),
    path(
        "shop/<slug:category_slug>/<slug:subcategory_slug>/<slug:lower_category_slug>/",
        ProductCategorytList.as_view(),
        name="product-list-by-category",
    ),
    path(
        "shop/<slug:category_slug>/<slug:subcategory_slug>/<slug:lower_category_slug>"
        "/<slug:product_slug>/",
        ProductDetail.as_view(),
        name="product-detail-by-category",
    ),
]
