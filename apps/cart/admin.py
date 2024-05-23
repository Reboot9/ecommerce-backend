"""
This module contains the admin configurations for the cart app.
"""

from django.contrib import admin
from django.core.cache import cache

from apps.cart.models import CartItem, Cart


class CartItemInline(admin.TabularInline):
    """Inline admin class for CartItem related to Cart."""

    model = CartItem
    extra = 2
    verbose_name = "Cart item"
    verbose_name_plural = "Cart items"
    autocomplete_fields = ("product",)


class CartAdmin(admin.ModelAdmin):
    """Admin class for Cart model."""

    inlines = [CartItemInline]
    list_display = (
        "id",
        "user",
        "total_quantity",
        "total_price",
        "created_at",
        "updated_at",
        "is_active",
    )
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("user__email",)
    search_help_text = "Search by user email"
    list_filter = ("is_active", "created_at", "updated_at")
    list_per_page = 10
    list_max_show_all = 100

    def save_model(self, request, obj, form, change):
        """
        Override save_model to invalidate cache when cart is saved.

        :param request: HttpRequest object
        :param obj: Cart instance being saved
        :param form: ModelForm instance
        :param change: Boolean indicating if this is a change (True) or a new object (False)
        """
        super().save_model(request, obj, form, change)

        # Invalidate the cart cache
        cart_id = obj.cart.id
        cache.delete(f"carts:{cart_id}:{request.path}?{request.GET.urlencode()}")

        # Invalidate related cart items cache
        cart_items = obj.cart_items.all()
        for item in cart_items:
            cache.delete(f"cart_item_detail:{request.path}?{request.GET.urlencode()}:{item.id}")
        cache.delete(f"cart_item_list:{request.path}?{request.GET.urlencode()}")

    def delete_model(self, request, obj):
        """
        Override delete_model to invalidate cache when cart is deleted.

        :param request: HttpRequest object
        :param obj: Cart instance being deleted
        """
        # Invalidate the cart cache
        cart_id = obj.id
        cache.delete(f"carts:{cart_id}:{request.path}?{request.GET.urlencode()}")

        # Invalidate related cart items cache
        cart_items = obj.cart_items.all()
        for item in cart_items:
            cache.delete(f"cart_item_detail:{request.path}?{request.GET.urlencode()}:{item.id}")
        cache.delete(f"cart_item_list:{request.path}?{request.GET.urlencode()}")

        super().delete_model(request, obj)


class CartItemAdmin(admin.ModelAdmin):
    """Admin class for CartItem model."""

    list_display = (
        "id",
        "cart",
        "product",
        "quantity",
        # "price",
        # "discount_percentage",
        "cost",
    )
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("cart",)
    autocomplete_fields = ("product", "cart")
    search_fields = ("product__name", "cart")
    search_help_text = "Search by product name, cart"
    list_filter = ("created_at", "updated_at")
    list_per_page = 10
    list_max_show_all = 100

    def save_model(self, request, obj, form, change):
        """
        Override save_model to invalidate cache when a cart item is saved.

        :param request: HttpRequest object
        :param obj: CartItem instance being saved
        :param form: ModelForm instance
        :param change: Boolean indicating if this is a change (True) or a new object (False)
        """
        super().save_model(request, obj, form, change)

        # Invalidate the cart item cache
        cache.delete(f"cart_item_detail:{request.path}?{request.GET.urlencode()}:{obj.id}")
        cache.delete(f"cart_item_list:{request.path}?{request.GET.urlencode()}")

        # Invalidate related cart cache
        cart_id = obj.cart.id
        cache.delete(f"carts:{cart_id}:{request.path}?{request.GET.urlencode()}")

    def delete_model(self, request, obj):
        """
        Override delete_model to invalidate cache when an cart item is deleted.

        :param request: HttpRequest object
        :param obj: CartITem instance being deleted
        """
        # Invalidate the cart item cache
        cache.delete(f"cart_item_detail:{request.path}?{request.GET.urlencode()}:{obj.id}")
        cache.delete(f"cart_item_list:{request.path}?{request.GET.urlencode()}")

        # Invalidate related cart cache
        cart_id = obj.cart.id
        cache.delete(f"carts:{cart_id}:{request.path}?{request.GET.urlencode()}")

        super().delete_model(request, obj)


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
