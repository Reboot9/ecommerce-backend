"""
Module defines Goods consumption model for warehouse app.
"""
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

    document = models.CharField(
        max_length=100,
        help_text=_("Consignment note"),
    )
    warehouse_item = models.ForeignKey(
        WarehouseItem,
        on_delete=models.CASCADE,
        related_name="consumptions",
        help_text=_("Product consumed"),
    )
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
        return (
            f"Consumption of {self.warehouse_item.product} - "
            f"Type: {self.get_consumption_type_display()}, Document: {self.document}"
        )
