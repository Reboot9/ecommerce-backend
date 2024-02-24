"""
Module defines Warehouse item model for warehouse app.
"""
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType


from apps.base.models import BaseID, BaseDate
from apps.product.models import Product


class WarehouseItem(BaseID, BaseDate):
    """
    Model that represents single product and used in warehouse operations.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=0,
        help_text=_("Quantity of the product"),
    )
    # Generic ForeignKey fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.UUIDField(blank=True, null=True)
    operation = GenericForeignKey("content_type", "object_id")

    class Meta:
        indexes = [models.Index(fields=["-created_at"]), models.Index(fields=["content_type"])]
        ordering = ["-created_at"]
        db_table = "warehouse_item"
        verbose_name = _("Warehouse Item")
        verbose_name_plural = _("Warehouse Items")

    def __str__(self):
        """
        Return a string representation of the Warehouse item model.

        :return: string representation of model
        """
        return f"{self.product.name} - Quantity: {self.quantity}"
