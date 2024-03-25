"""
This module contains Cart item API views for the cart app.
"""
from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.cart.serializers import CartItemSerializer
from apps.cart.services.cartitem import get_cartitem_detail, delete_cart_item


class CartItemViewSet(viewsets.ModelViewSet):
    """CartItem API handler."""

    http_method_names = ["get", "delete"]
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return the queryset for the view."""
        if self.action in {"retrieve", "destroy"}:
            return get_cartitem_detail(pk=self.kwargs["pk"])

    def destroy(self, request, *args, **kwargs):
        """Delete a CartItem."""
        instance = self.get_object()
        cart = instance.cart
        delete_cart_item(instance, cart)
        return Response(status=status.HTTP_204_NO_CONTENT)
