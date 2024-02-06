"""
Module: urls.py.

This module contains urls for the order app.
"""
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.order.views.order import OrderViewSet

order_router = SimpleRouter()
order_router.register(prefix="orders", viewset=OrderViewSet, basename="orders")

app_name = "order"

urlpatterns = [
    path("", include(order_router.urls)),
]
