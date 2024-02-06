"""
Module: views.py.

This module contains handler for the order app.
"""
from rest_framework import viewsets, permissions

from apps.order.models.order import Order
from apps.order.serializers.order import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """Handlers for operation with order."""

    http_method_names = ["get", "post"]
    serializer_class = OrderSerializer

    def get_permissions(self):
        """Use different permissions."""
        if self.action in {"list", "retrieve"}:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Different filters require different sets of queries."""
        user = self.request.user
        if self.action == "list":
            return Order.objects.filter(email=user.email)
        if self.action in {"retrieve"}:
            return Order.objects.filter(email=user.email, pk=self.kwargs["pk"])
