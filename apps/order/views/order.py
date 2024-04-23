"""
This module contains handlers for the order app.
"""
from django.shortcuts import get_object_or_404
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
        """Get orders based on the user's email."""
        user = self.request.user
        return Order.objects.filter(email=user.email)

    def get_object(self):
        """
        Retrieve a single order based on the user and order ID.
        """
        user = self.request.user
        return get_object_or_404(Order, email=user.email, pk=self.kwargs.get("pk"))
