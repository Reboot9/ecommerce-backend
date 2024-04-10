"""
URLs for the cart app.
"""
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.cart.views import CartViewSet, CartItemViewSet

router = SimpleRouter()
router.register(prefix=r"carts/items", viewset=CartItemViewSet, basename="cart_items")
router.register(prefix=r"carts", viewset=CartViewSet, basename="carts")

app_name = "cart"

urlpatterns = [
    path("", include(router.urls)),
]
