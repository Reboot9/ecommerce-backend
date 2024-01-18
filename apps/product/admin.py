"""
Module: admin.py.

This module contains the admin configurations for the product app.
"""

from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext

from apps.product.models import Manufacturer, Category, Image
from apps.product.models.product import ProductCharacteristics, TypeProductCharacteristics, Product


class TypeProductCharacteristicsInline(admin.TabularInline):
    """Inline class for TypeProductCharacteristics related to Product."""

    model = TypeProductCharacteristics.product.through
    extra = 1
    verbose_name = "Type of product characteristic"
    verbose_name_plural = "Type of product characteristics"


class ProductCharacteristicsInline(admin.TabularInline):
    """Inline admin class for ProductCharacteristics related to Product."""

    model = ProductCharacteristics.product.through
    extra = 1
    verbose_name = "Product Characteristic"
    verbose_name_plural = "Product Characteristics"


class ImageInline(admin.TabularInline):
    """Inline admin class for Image related to Product."""

    model = Image
    extra = 2
    verbose_name = "Additional image"
    verbose_name_plural = "Additional images"


class ProductAdmin(admin.ModelAdmin):
    """Admin class for Product model."""

    @admin.action(description="Remove promotional discount")
    def remove_discount(self, request, queryset):
        """Custom admin action to remove promotional discount."""
        updated = queryset.update(discount_percentage=0)
        self.message_user(
            request,
            ngettext(
                "%d discount successfully removed.", "%d discounts successfully removed.", updated
            )
            % updated,
            messages.SUCCESS,
        )

    list_display = (
        "slug",
        "name",
        "price",
        "stock",
        "manufacturer",
        "categories",
        "discount_percentage",
        "price_discount",
        "created_at",
        "updated_at",
    )
    list_select_related = ("manufacturer", "categories")
    readonly_fields = ("created_at", "updated_at")
    search_fields = (
        "name",
        "product_code",
        "slug",
        "manufacturer__trade_brand",
        "categories__name",
    )
    list_filter = ("stock", "discount_percentage", "created_at", "updated_at")
    list_editable = ("price", "discount_percentage", "stock")
    prepopulated_fields = {"slug": ("name", "product_code")}
    actions = ("remove_discount",)
    inlines = (
        ProductCharacteristicsInline,
        TypeProductCharacteristicsInline,
        ImageInline,
    )  # inline will change
    list_per_page = 10
    list_max_show_all = 100


class ProductCharacteristicsAdmin(admin.ModelAdmin):
    """Admin class for ProductCharacteristics model."""

    list_display = ("product_characteristic", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("product_characteristic",)
    list_filter = ("created_at", "updated_at")
    filter_horizontal = ("product",)
    list_per_page = 10
    list_max_show_all = 100


class TypeProductCharacteristicsAdmin(admin.ModelAdmin):
    """Admin class for TypeProductCharacteristics model."""

    list_display = ("type_characteristic", "product_characteristics", "created_at", "updated_at")
    list_select_related = ("product_characteristics",)
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("type_characteristic",)
    list_filter = ("created_at", "updated_at")
    filter_horizontal = ("product",)
    list_per_page = 10
    list_max_show_all = 100


class ManufacturerAdmin(admin.ModelAdmin):
    """Admin class for Manufacturer mode."""

    list_display = (
        "trade_brand",
        "country",
        "country_brand_registration",
        "created_at",
        "updated_at",
    )
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("trade_brand", "country")
    list_filter = ("created_at", "updated_at")
    list_per_page = 10
    list_max_show_all = 100


class CategoryAdmin(admin.ModelAdmin):
    """Admin class for Category model."""

    list_display = (
        "id",
        "name",
    )


class ImageAdmin(admin.ModelAdmin):
    """Admin class for Image model."""

    list_display = ("image", "product", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("product__name",)
    list_filter = ("created_at", "updated_at")
    list_per_page = 10
    list_max_show_all = 100


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCharacteristics, ProductCharacteristicsAdmin)
admin.site.register(TypeProductCharacteristics, TypeProductCharacteristicsAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Image, ImageAdmin)
