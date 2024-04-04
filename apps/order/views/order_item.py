"""
This module contains handlers for the OrderItem model.
"""
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

from apps.order.models.order_item import OrderItem
from apps.order.serializers.order_item import OrderItemSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle operations on OrderItem.
    """

    http_method_names = [
        "get",
        "post",
    ]
    serializer_class = OrderItemSerializer

    def get_permissions(self):
        """Set permissions based on the action."""
        if self.action in [
            "list",
            "retrieve",
        ]:
            # Allow access only to authenticated users for listing and retrieving order items.
            return [permissions.IsAuthenticated()]
        else:
            # Allow any user to perform other actions.
            return [permissions.AllowAny()]

    def get_queryset(self):
        """Get order items based on the action and user."""
        user = self.request.user
        return OrderItem.objects.filter(
            order__pk=self.kwargs.get("order_id"), order__email=user.email
        )

    def get_object(self):
        """
        Retrieve a single order item based on the user and item ID.
        """
        user = self.request.user
        return get_object_or_404(
            OrderItem,
            order__email=user.email,
            order__pk=self.kwargs.get("order_id"),
            pk=self.kwargs.get("pk"),
        )

    def perform_create(self, serializer):
        """Associate newly created order item with the user."""
        serializer.save(order__user=self.request.user)
