"""
This module contains handlers for the OrderItem model.
"""
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from apps.base.mixins import CachedListMixin, CACHE_TTL
from apps.order.models.order import Order
from apps.order.models.order_item import OrderItem
from apps.order.serializers.order_item import OrderItemSerializer


class OrderItemViewSet(CachedListMixin, viewsets.ModelViewSet):
    """
    ViewSet to handle operations on OrderItem.
    """

    http_method_names = ["get", "post", "patch", "head", "options", "trace"]
    serializer_class = OrderItemSerializer

    def get_cache_key(self, order_item_id=None) -> str:
        """
        Method to get cache key.

        :return: cache key for the order items.
        """
        base_key = self.request.path
        if self.request.GET:
            base_key += f"?{self.request.GET.urlencode()}"
        if order_item_id is not None:
            return f"order_item_detail:{base_key}:{order_item_id}"
        return f"order_item_list:{base_key}"

    def get_permissions(self):
        """Set permissions based on the action."""
        if self.action in ["list", "retrieve"]:
            # Allow access only to authenticated users for listing and retrieving order items.
            return [permissions.IsAuthenticated()]
        elif self.action in ["partial_update", "create"]:
            return [permissions.IsAdminUser()]
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
        """Associate newly created order item with the order."""
        order_id = self.kwargs.get("order_id")
        order_instance = get_object_or_404(Order, id=order_id)

        order_item = serializer.save(order=order_instance)
        order_instance.items.add(order_item)
        order_instance.save()

        # Clear the list cache when a new order item is created
        cache.delete(f"order_item_list:{self.request.path}?{self.request.GET.urlencode()}")

        # Invalidate related order cache
        cache.delete(
            f"orders_detail:{self.request.path}?{self.request.GET.urlencode()}:{order_id}"
        )
        cache.delete(f"orders_list:{self.request.path}?{self.request.GET.urlencode()}")
        return order_instance

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific order item instance.
        """
        order_item_id = self.kwargs.get("pk")
        cache_key = self.get_cache_key(order_item_id)
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        cache.set(cache_key, data, timeout=CACHE_TTL)

        return Response(data)

    def perform_update(self, serializer) -> None:
        """
        Perform actions when updating Order instance.

        :param serializer: The serializer instance used for validation and saving.
        :return:
        """
        instance = serializer.save()
        request_path = self.request.path
        # Invalidate order item cache
        cache.delete(self.get_cache_key(order_item_id=instance.id))
        cache.delete(f"order_item_list:{request_path}?{self.request.GET.urlencode()}")

        # Invalidate related order cache
        order_id = instance.order.id
        cache.delete(f"orders_detail:{request_path}?{self.request.GET.urlencode()}:{order_id}")
        cache.delete(f"orders_list:{request_path}?{self.request.GET.urlencode()}")

        return instance

    def perform_destroy(self, instance) -> None:
        """
        Perform actions when deleting an Order Item instance.

        :param instance: instance to be destroyed.
        """
        # clear cache before deleting an instance
        request_path = self.request.path
        # Invalidate order item cache
        cache.delete(self.get_cache_key(order_item_id=instance.id))
        cache.delete(f"order_item_list:{request_path}?{self.request.GET.urlencode()}")

        # Invalidate related order cache
        order_id = instance.order.id
        cache.delete(f"orders_detail:{request_path}?{self.request.GET.urlencode()}:{order_id}")
        cache.delete(f"orders_list:{request_path}?{self.request.GET.urlencode()}")

        instance.delete()
