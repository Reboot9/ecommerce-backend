"""
Module defines Category model for product app.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseDate, BaseID


class Category(BaseID, BaseDate):
    """Represents a product category in the ecommerce system."""

    name = models.CharField(max_length=256, verbose_name=_("Name"), db_index=True)
    slug = models.SlugField(max_length=256, unique=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories"
    )
    level = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "category"
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["level", "name"]

    def __str__(self) -> str:
        """
        Return a string representation of the Category model.

        :return: The name of category.
        """
        return self.name

    def get_ancestors(self) -> list:
        """
        Retrieve the ancestors of the category.

        This method doesn't involve additional queries, as it simply traverses the parent
        hierarchy.

        :return: Category objects representing the ancestors.
        """
        ancestors = []
        current = self.parent

        # Traverse the parent hierarchy to collect ancestors.
        while current:
            ancestors.append(current)
            current = current.parent

        return ancestors

    def get_descendants(self) -> list:
        """
        Retrieve the descendants of the category.

        Note that deep hierarchies or a large number of descendants may cause performance issues

        :return: Category objects representing the descendants.
        """
        descendants = list(
            self.subcategories.all()
            .select_related("subcategories")
            .prefetch_related("subcategories")
        )

        # Recursively fetch descendants for each subcategory.
        for descendant in descendants:
            descendants.extend(descendant.get_descendants())

        return descendants
