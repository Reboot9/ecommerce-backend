"""
This module contains necessary Cart views for the cart app.
"""
from django.core.cache import cache
from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.base.mixins import CACHE_TTL
from apps.cart.models import Cart
from apps.cart.serializers import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    """Cart management API."""

    http_method_names = ["get", "delete", "head", "options", "trace"]
    serializer_class = CartSerializer

    def get_permissions(self):
        """Set permissions based on the action."""
        if self.action in ["destroy"]:
            return [permissions.IsAdminUser()]

        return [permissions.IsAuthenticated()]

    def get_cache_key(self, cart_id) -> str:
        """
        Method to get cache key for the cart list.

        :return: cache key for the cart.
        """
        return f"carts:{cart_id}:{self.request.path}?{self.request.GET.urlencode()}"

    def get_queryset(self):
        """
        Retrieves the queryset of carts based on the user.

        :return: The queryset of carts filtered by the user.
        """
        user = self.request.user
        # Logic to filter carts based on the user
        queryset = Cart.objects.filter(user=user, is_active=True)
        return queryset

    def list(self, request, *args, **kwargs) -> Response:
        """
        Override the list method to add caching.
        """
        cart = Cart.objects.filter(user=self.request.user, is_active=True).first()
        cache_key = self.get_cache_key(cart.id)
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=CACHE_TTL)
        return response

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
        cart_instance = self.get_object()
        cart_instance.is_active = False
        cart_instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        """
        Override perform_destroy to clear cache after deleting a cart.
        """
        # Clear the list cache when a cart is deleted
        cache.delete(self.get_cache_key(instance.id))

    def perform_create(self, serializer):
        """
        Perform actions when creating instance.

        :param serializer: The serializer instance used for validation and saving.
        :return:
        """
        instance = serializer.save()
        cache.delete(self.get_cache_key(instance.id))
        return instance

    def perform_update(self, serializer):
        """
        Override perform_update to clear cache after updating a cart item.

        :param serializer: The serializer instance used for validation and saving.
        """
        instance = serializer.save()
        # Clear the list cache when a cart item is updated
        cache.delete(self.get_cache_key(instance.id))
        return instance
