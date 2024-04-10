"""
This module contains Cart item API views for the cart app.
"""
from django.shortcuts import get_object_or_404
from rest_framework import permissions, mixins
from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.cart.models import CartItem, Cart
from apps.cart.serializers import CartItemSerializer
from apps.cart.services.cart_item import delete_cart_item


class CartItemViewSet(viewsets.ModelViewSet, mixins.CreateModelMixin):
    """CartItem API handler."""

    # http_method_names = ["get", "put", "patch", "delete",]
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return the queryset for the view."""
        user = self.request.user
        cart = get_object_or_404(Cart, user=user, is_active=True)
        return CartItem.objects.select_related("cart", "product").filter(cart=cart)

    def get_object(self):
        """
        Retrieves a specific CartItem object.

        :return: requested CartItem instance.
        """
        user = self.request.user
        # Logic to filter cart items based on the user
        cart = get_object_or_404(Cart, user=user, is_active=True)
        return get_object_or_404(
            CartItem.objects.select_related("cart", "product"),
            pk=self.kwargs.get("pk"),
            cart=cart,
        )

    def create(self, request, *args, **kwargs):
        """
        Create a new CartItem instance.

        :param request: HTTP request object.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """
        cart, _ = Cart.objects.get_or_create(user=self.request.user, is_active=True)
        context = {
            "cart": cart,
        }
        serializer = self.get_serializer(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        Update only the quantity field of a CartItem.

        :param request: HTTP request.
        :return: HTTP response with updated CartItem data or error.
        """
        instance = self.get_object()
        serializer = CartItemSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        """
        Delete CartItem instance.
        """
        instance = self.get_object()
        cart = instance.cart
        delete_cart_item(instance, cart)
        return Response(status=status.HTTP_204_NO_CONTENT)
