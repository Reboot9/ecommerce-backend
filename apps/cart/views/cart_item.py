"""
This module contains Cart item API views for the cart app.
"""
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import permissions, mixins
from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.base.mixins import CachedListMixin, CACHE_TTL
from apps.cart.models import CartItem, Cart
from apps.cart.serializers import CartItemSerializer
from apps.cart.services.cart_item import delete_cart_item


class CartItemViewSet(CachedListMixin, viewsets.ModelViewSet, mixins.CreateModelMixin):
    """CartItem API handler."""

    # http_method_names = ["get", "put", "patch", "delete",]
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_cache_key(self, cart_item_id=None) -> str:
        """
        Method to get cache key.

        :return: cache key for the cart items.
        """
        base_key = self.request.path
        if self.request.GET:
            base_key += f"?{self.request.GET.urlencode()}"
        if cart_item_id is not None:
            return f"cart_item_detail:{base_key}:{cart_item_id}"
        return f"cart_item_list:{base_key}"

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

    def retrieve(self, request, *args, **kwargs):
        """Retrieve cart item instance."""
        cart_item_id = self.kwargs.get("pk")
        cache_key = self.get_cache_key(cart_item_id)
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        cache.set(cache_key, data, timeout=CACHE_TTL)

        return Response(data)

    def partial_update(self, request, *args, **kwargs):
        """
        Update only the quantity field of a CartItem.

        :param request: HTTP request.
        :return: HTTP response with updated CartItem data or error.
        """
        instance = self.get_object()
        serializer = CartItemSerializer(instance, data=request.data, partial=True)
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

    def perform_create(self, serializer):
        """
        Perform actions when creating instance.

        :param serializer: The serializer instance used for validation and saving.
        :return:
        """
        instance = serializer.save()
        # Clear the list cache when a new cart item is created
        cache.delete(f"cart_item_list:{self.request.path}?{self.request.GET.urlencode()}")
        cart_id = instance.cart.id
        # Invalidate related cart cache
        cache.delete(f"carts:{cart_id}:{self.request.path}?{self.request.GET.urlencode()}")
        return instance

    def perform_update(self, serializer) -> None:
        """
        Perform actions when updating Cart Item instance.

        :param serializer: The serializer instance used for validation and saving.
        :return:
        """
        instance = serializer.save()
        request_path = self.request.path

        # Invalidate cart item cache
        cache.delete(self.get_cache_key(instance.id))
        cache.delete(f"cart_item_list:{request_path}?{self.request.GET.urlencode()}")

        # Invalidate related cart cache
        cart_id = instance.cart.id
        cache.delete(f"carts:{cart_id}:{self.request.path}?{self.request.GET.urlencode()}")

        return instance

    def perform_destroy(self, instance):
        """
        Perform actions when deleting an Cart Item instance.

        :param instance: instance to be destroyed.
        """
        # clear cache before deleting an instance
        request_path = self.request.path
        # Invalidate cart item cache
        cache.delete(self.get_cache_key(instance.id))
        cache.delete(f"cart_item_list:{request_path}?{self.request.GET.urlencode()}")

        # Invalidate related cart cache
        cart_id = instance.cart.id
        cache.delete(f"carts:{cart_id}:{self.request.path}?{self.request.GET.urlencode()}")

        instance.delete()
