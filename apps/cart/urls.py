"""
URLs for the cart app.
"""
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.cart.views import CartViewSet, CartItemViewSet

cart_router = SimpleRouter()
cart_router.register(prefix="carts", viewset=CartViewSet, basename="carts")

cart_item_router = SimpleRouter()
cart_item_router.register(prefix="cart_items", viewset=CartItemViewSet, basename="cart_items")

app_name = "cart"

urlpatterns = [
    path("", include(cart_router.urls)),
    path("", include(cart_item_router.urls)),
]
