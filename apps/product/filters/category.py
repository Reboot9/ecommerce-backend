"""
Category-related filters for product app.
"""
from typing import Any

from apps.product.models import Category
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class BaseSubcategoryFilter(admin.SimpleListFilter):
    """
    Base class for filtering categories and their subcategories in django admin.
    """

    title = _("Category")
    parameter_name = "parent_category"

    def lookups(self, request, model_admin: Any) -> list[tuple[str, str]]:
        """
        Returns a list of tuples representing the available filter options.

        :param request: http request object.
        :param model_admin: admin instance for the model.

        :return: list of tuples containing category ids and names.
        """
        categories = Category.objects.all()

        return [(str(category.id), category) for category in categories]

    def queryset(self, request, queryset):
        """
        Filters the queryset based on selected category or subcategory.

        :param request: http request object.
        :param queryset: queryset to filter.
        :return: filtered queryset
        """
        if self.value():
            category = Category.objects.get(pk=self.value())
            subcategories = list(category.get_descendants()) + [category]

            return queryset.filter(parent_id__in=subcategories)


class ProductSubcategoryFilter(BaseSubcategoryFilter):
    """
    Filter for products based on categories and their subcategories.
    """

    def queryset(self, request, queryset):
        """
        Filters the queryset of products based on selected categories or subcategories.

        :param request: http request object.
        :param queryset: queryset to filter.
        :return: filtered queryset
        """
        if self.value():
            category = Category.objects.get(pk=self.value())
            subcategories = list(category.get_descendants()) + [category]

            return queryset.filter(categories__in=subcategories)
