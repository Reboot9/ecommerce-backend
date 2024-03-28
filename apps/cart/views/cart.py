"""
This module contains necessary Cart views for the cart app.
"""
from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.cart.serializers import CartSerializer
from apps.cart.services.cart import get_cart_detail, deactivate_cart


class CartViewSet(viewsets.ModelViewSet):
    """Cart management API."""

    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return the queryset for the view."""
        if self.action in {"retrieve", "partial_update", "destroy"}:
            return get_cart_detail(pk=self.kwargs["pk"])

    def create(self, request, *args, **kwargs):
        """Create a new cart."""
        serializer = self.serializer_class(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Delete a cart."""
        instance = self.get_object()
        deactivate_cart(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)