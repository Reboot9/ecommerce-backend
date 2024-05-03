"""
This module contains handlers for the order app.
"""
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.base.pagination import PaginationCommon
from apps.order.models.order import Order
from apps.order.serializers.order import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """Handlers for operation with order."""

    http_method_names = [
        "get",
        "post",
        "patch",
    ]
    serializer_class = OrderSerializer
    pagination_class = PaginationCommon

    def get_permissions(self):
        """Set permissions based on the action."""
        if self.action in ["list", "retrieve"]:
            # Allow access only to authenticated users for listing and retrieving orders.
            return [permissions.IsAuthenticated()]
        elif self.action in ["patch"]:
            return [permissions.IsAdminUser()]
        else:
            # Allow any user to perform other actions.
            return [permissions.AllowAny()]

    def get_queryset(self):
        """Get orders based on the user's email."""
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                return Order.objects.all()
            return Order.objects.filter(email=user.email)
        else:
            # return an empty queryset if user is not authenticated
            return Order.objects.none()

    def get_object(self):
        """
        Retrieve a single order based on the user and order ID.
        """
        user = self.request.user
        order_id = self.kwargs.get("pk")

        if not isinstance(user, AnonymousUser):
            # If the user is authenticated, retrieve the order based on the user's email
            return get_object_or_404(Order, email=user.email, pk=order_id)
        else:
            # If the user is not authenticated, retrieve the order based on the email
            # provided in the order data
            order_email = self.request.data.get("email")
            if not order_email:
                raise ValidationError("Email is required for unauthenticated requests.")
            return get_object_or_404(Order, email=order_email, pk=order_id)

    def create(self, request, *args, **kwargs):
        """Handle creating a new order."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
