"""
This module contains necessary Cart views for the cart app.
"""
from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.cart.models import Cart
from apps.cart.serializers import CartSerializer
from apps.cart.services.cart import deactivate_empty_cart


class CartViewSet(viewsets.ModelViewSet):
    """Cart management API."""

    http_method_names = ["get", "destroy"]
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Retrieves the queryset of carts based on the user.

        :return: The queryset of carts filtered by the user.
        """
        user = self.request.user
        # Logic to filter carts based on the user
        queryset = Cart.objects.filter(user=user, is_active=True)
        return queryset

    def get_object(self):
        """
        Retrieves a specific cart object.

        :return: specific Cart object.
        """
        return (
            Cart.objects.prefetch_related("items")
            .select_related("user")
            .get(pk=self.kwargs.get("pk"), is_active=True)
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves a specific cart instance.

        This method is not allowed for this endpoint and will return a response indicating
        the disallowed action.

        :param request: HTTP request object.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """
        return Response(
            {"detail": "Retrieve is not allowed for this endpoint."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def create(self, request, *args, **kwargs):
        """
        Create a new cart instance.

        :param request: HTTP request object.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """
        serializer = self.serializer_class(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a cart instance.

        :param request: HTTP request object.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """
        instance = self.get_object()
        deactivate_empty_cart(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
