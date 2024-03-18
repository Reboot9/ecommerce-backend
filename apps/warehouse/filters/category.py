"""
Category-related filters for warehouse app.
"""
from apps.product.filters.category import BaseSubcategoryFilter
from apps.product.models import Category


class WarehouseSubcategoryFilter(BaseSubcategoryFilter):
    """
    Filter for products based on categories and their subcategories.
    """

    def queryset(self, request, queryset):
        """
        Filters the queryset of warehouse items based on selected categories or subcategories.

        :param request: http request object.
        :param queryset: queryset to filter.
        :return: filtered queryset
        """
        if self.value():
            category = Category.objects.get(pk=self.value())
            subcategories = list(category.get_descendants()) + [category]

            return queryset.filter(product__categories__in=subcategories)
