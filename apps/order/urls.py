"""
URLs for the order app.
"""
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.order.views.order import OrderViewSet
from apps.order.views.order_item import OrderItemViewSet

router = SimpleRouter()
router.register(r"orders", OrderViewSet, basename="orders")
router.register(r"orders/(?P<order_id>[^/.]+)/items", OrderItemViewSet, basename="order-items")

app_name = "order"

urlpatterns = [
    path("", include(router.urls)),
]
