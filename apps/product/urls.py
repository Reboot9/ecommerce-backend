"""
Module: urls.py.

This module contains urls for the product app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.product.views.product import ProductSet

product_router = DefaultRouter()
product_router.register(prefix="products", viewset=ProductSet, basename="product")

app_name = "product"

urlpatterns = [
    path("", include(product_router.urls)),
]
