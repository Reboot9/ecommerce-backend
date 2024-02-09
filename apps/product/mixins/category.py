"""
This module contains custom Category-related mixins.
"""
from typing import Tuple

from django.shortcuts import get_object_or_404

from apps.product.models import Category


class CategoryMixin:
    """
    A mixin for views handling hierarchical categories.

    This mixin provides a method to retrieve category, subcategory, and lower-level category
    objects based on slugs provided in the URL kwargs.
    """

    def get_categories(self) -> Tuple[Category, Category, Category]:
        """
        Retrieve category, subcategory, and lower-level category objects based on URL kwargs.

        :return: A tuple containing category, subcategory, and lower-level category objects.
        If any category is not found, a 404 response is raised.
        """
        category_slug = self.kwargs.get("category_slug")
        subcategory_slug = self.kwargs.get("subcategory_slug")
        lower_category_slug = self.kwargs.get("lower_category_slug")

        category = get_object_or_404(Category, slug=category_slug)
        subcategory = get_object_or_404(Category, parent=category, slug=subcategory_slug)
        lower_category = get_object_or_404(Category, parent=subcategory, slug=lower_category_slug)

        return category, subcategory, lower_category
