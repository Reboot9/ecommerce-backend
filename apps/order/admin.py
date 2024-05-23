"""
Module: admin.py.

This module contains the admin configurations for the order app.
"""

from django.contrib import admin
from django.core.cache import cache

from apps.order.forms import DeliveryModelAdminForm
from apps.order.models.delivery import Delivery
from apps.order.models.order import Order
from apps.order.models.order_item import OrderItem


class DeliveryInline(admin.TabularInline):
    """Inline admin class for Delivery related to Order."""

    model = Delivery
    verbose_name = "Delivery"
    verbose_name_plural = "Deliveries"


class OrderItemInline(admin.TabularInline):
    """Inline admin class for OrderItem related to Order."""

    model = OrderItem
    extra = 2
    autocomplete_fields = ("product",)
    verbose_name = "Order item"
    verbose_name_plural = "Order Items"


class OrderAdmin(admin.ModelAdmin):
    """Admin class for Order model."""

    list_display = (
        "order_number",
        "first_name",
        "last_name",
        "status",
        "phone",
        "email",
        "comment",
        "total_order_price",
        "is_paid",
        "created_at",
        "updated_at",
    )
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("first_name", "last_name", "phone", "email")
    search_help_text = (
        "In this field you can search by such fields: first_name" "last_name, phone, email"
    )
    list_filter = ("status", "is_paid", "created_at", "updated_at")
    list_editable = ("status", "is_paid")
    inlines = (OrderItemInline,)
    list_per_page = 10
    list_max_show_all = 100

    def save_model(self, request, obj, form, change):
        """
        Override save_model to invalidate cache when an order is saved.

        :param request: HttpRequest object
        :param obj: Order instance being saved
        :param form: ModelForm instance
        :param change: Boolean indicating if this is a change (True) or a new object (False)
        """
        super().save_model(request, obj, form, change)

        # Invalidate the order cache
        cache.delete(f"orders_detail:{request.path}?{request.GET.urlencode()}:{obj.id}")
        cache.delete(f"orders_list:{request.path}?{request.GET.urlencode()}")

        # Invalidate related order items cache
        order_items = obj.order_items.all()
        for item in order_items:
            cache.delete(f"order_item_detail:{request.path}?{request.GET.urlencode()}:{item.id}")
        cache.delete(f"order_item_list:{request.path}?{request.GET.urlencode()}")

    def delete_model(self, request, obj):
        """
        Override delete_model to invalidate cache when an order is deleted.

        :param request: HttpRequest object
        :param obj: Order instance being deleted
        """
        # Invalidate the order cache
        cache.delete(f"orders_detail:{request.path}?{request.GET.urlencode()}:{obj.id}")
        cache.delete(f"orders_list:{request.path}?{request.GET.urlencode()}")

        # Invalidate related order items cache
        order_items = obj.order_items.all()
        for item in order_items:
            cache.delete(f"order_item_detail:{request.path}?{request.GET.urlencode()}:{item.id}")
        cache.delete(f"order_item_list:{request.path}?{request.GET.urlencode()}")

        super().delete_model(request, obj)


class OrderItemAdmin(admin.ModelAdmin):
    """Admin class for OrderItem model."""

    list_display = (
        "order",
        "discount_percentage",
        "price",
        "product",
        "quantity",
        "order_item_cost",
        "created_at",
        "updated_at",
    )
    list_select_related = ("order",)
    autocomplete_fields = ("product",)  # only ForeignKey or ManyToMany
    list_filter = ("created_at", "updated_at")
    search_fields = ("product", "order")
    search_help_text = "In this field you can search by such fields: product, order"
    list_per_page = 10
    list_max_show_all = 100

    def save_model(self, request, obj, form, change):
        """
        Override save_model to invalidate cache when an order item is saved.

        :param request: HttpRequest object
        :param obj: OrderItem instance being saved
        :param form: ModelForm instance
        :param change: Boolean indicating if this is a change (True) or a new object (False)
        """
        super().save_model(request, obj, form, change)

        # Invalidate the order item cache
        cache.delete(f"order_item_detail:{request.path}?{request.GET.urlencode()}:{obj.id}")
        cache.delete(f"order_item_list:{request.path}?{request.GET.urlencode()}")

        # Invalidate related order cache
        order_id = obj.order.id
        cache.delete(f"orders_detail:{request.path}?{request.GET.urlencode()}:{order_id}")
        cache.delete(f"orders_list:{request.path}?{request.GET.urlencode()}")

    def delete_model(self, request, obj):
        """
        Override delete_model to invalidate cache when an order item is deleted.

        :param request: HttpRequest object
        :param obj: OrderItem instance being deleted
        """
        # Invalidate the order item cache
        cache.delete(f"order_item_detail:{request.path}?{request.GET.urlencode()}:{obj.id}")
        cache.delete(f"order_item_list:{request.path}?{request.GET.urlencode()}")

        # Invalidate related order cache
        order_id = obj.order.id
        cache.delete(f"orders_detail:{request.path}?{request.GET.urlencode()}:{order_id}")
        cache.delete(f"orders_list:{request.path}?{request.GET.urlencode()}")

        super().delete_model(request, obj)


class DeliveryAdmin(admin.ModelAdmin):
    """Admin class for Delivery model."""

    form = DeliveryModelAdminForm
    list_display = ("id", "city", "option", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at", "option")
    search_fields = ("city", "option")
    search_help_text = "In this field you can search by such fields: city, option"
    list_per_page = 10
    list_max_show_all = 100


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Delivery, DeliveryAdmin)
