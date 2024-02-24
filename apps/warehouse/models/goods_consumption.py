"""
Module defines Goods consumption model for warehouse app.
"""
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseDate, BaseID
from apps.warehouse.models.warehouse_item import WarehouseItem


class GoodsConsumption(BaseID, BaseDate):
    """
    Represents the consumption of products to the warehouse.
    """

    class ConsumptionTypeChoices(models.TextChoices):
        """Enum for arrival types."""

        ORDER = (
            "order",
            _("Order"),
        )
        WRITE_OFF = (
            "write-off",
            _("Write-off"),
        )

    warehouse_items = GenericRelation(WarehouseItem)
    consumption_type = models.CharField(
        max_length=50,
        choices=ConsumptionTypeChoices.choices,
        help_text=_("Type of consumption"),
    )
    comment = models.TextField(
        blank=True,
        null=True,
        help_text=_("Additional comments"),
        max_length=2000,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        db_table = "goods_consumption"
        verbose_name = _("Goods Consumption")
        verbose_name_plural = _("Goods Consumptions")

    def __str__(self):
        """
        Return a string representation of the Goods consumption model.

        :return: string representation of model
        """
        warehouse_items_str = ", ".join(str(item) for item in self.warehouse_items.all())
        return (
            f"Consumption Type: {self.consumption_type}, Document: {self.consignmentnote}, "
            f"Warehouse Items: [{warehouse_items_str}]"
        )
