"""
This module contains handlers for the order app.
"""
from rest_framework import viewsets, permissions

from apps.order.models.order import Order
from apps.order.serializers.order import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """Handlers for operation with order."""

    http_method_names = ["get", "post"]
    serializer_class = OrderSerializer

    def get_permissions(self):
        """Set permissions based on the action."""
        if self.action in ["list", "retrieve"]:
            # Allow access only to authenticated users for listing and retrieving orders.
            return [permissions.IsAuthenticated()]
        else:
            # Allow any user to perform other actions.
            return [permissions.AllowAny()]

    def get_queryset(self):
        """Get orders based on the action and user."""
        user = self.request.user
        if self.action == "list":
            # Filter orders for listing based on the user's email.
            return Order.objects.filter(email=user.email)
        elif self.action == "retrieve":
            # Filter single order retrieval based on the user's email and order ID.
            return Order.objects.filter(email=user.email, pk=self.kwargs["pk"])
