"""
Module defines Category model for product app.
"""
from typing import Type, List

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseDate, BaseID


class Category(BaseID, BaseDate):
    """Represents a product category in the ecommerce system."""

    LEVEL_CHOICES = [
        (0, _("Top Level")),
        (1, _("Medium Level")),
        (2, _("Lower Level")),
    ]

    name = models.CharField(max_length=256, verbose_name=_("Name"), db_index=True)
    slug = models.SlugField(max_length=256, unique=False)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories"
    )
    level = models.PositiveSmallIntegerField(
        choices=LEVEL_CHOICES,
        default=0,
        verbose_name=_(
            "Category Level",
        ),
        help_text=_(
            "Select the level of this category. "
            "Top Level is for main categories, "
            "Medium Level for subcategories, "
            "and Lower Level for the most specific categories."
        ),
    )

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
        parent_category = f" ({self.parent})" if self.parent else ""
        return f"{self.name}{parent_category}"

    def clean(self) -> None:
        """
        Override default method to enforce custom validation rules.
        """
        super().clean()

        if self.level in [1, 2] and not self.parent_id:
            raise ValidationError(
                {"parent": _('Categories with level "Medium" and "Lower" need to have a parent.')}
            )

        if self.parent_id and (self.level <= self.parent.level):
            # Despite checking that level <= parent.level, the error message mentions category
            # level must be lower than its parent's level.
            raise ValidationError(
                {"parent": _("Category level must be lower than its parent's category level.")}
            )

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
        descendants = list(self.subcategories.all())

        # Recursively fetch descendants for each subcategory.
        for descendant in descendants:
            descendants.extend(descendant.get_descendants())

        return descendants

    @classmethod
    def get_descendants_by_level(
        cls: Type["Category"], slug: str, *, level: int
    ) -> List["Category"]:
        """
        Retrieve descendants of a category with a specified level.

        :param slug: slug of parent category.
        :param level: desired level of descendants (0 for top-level, 1 for medium, 2 for lower).
        :return: A QuerySet containing the descendants of the specified category at
         the specified level.
         An empty QuerySet is returned if the level is not in the range [0, 2].
        """
        if level in {i for i in range(3)}:
            return cls.objects.filter(parent__slug=slug, level=level)
        return cls.objects.none()
