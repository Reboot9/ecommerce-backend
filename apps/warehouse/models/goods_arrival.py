"""
Module defines Goods arrival model for warehouse app.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseDate, BaseID
from apps.warehouse.models.warehouse_item import WarehouseItem


class GoodsArrival(BaseID, BaseDate):
    """
    Represents the arrival of products to the warehouse.
    """

    class ArrivalTypeChoices(models.TextChoices):
        """Enum for arrival types."""

        ARRIVAL = (
            "arrival",
            _("Arrival"),
        )
        RETURN = (
            "return",
            _("Return"),
        )
        INVENTORY = (
            "inventory",
            _("Inventory"),
        )

    document = models.CharField(  # has to be unique
        max_length=100,  # 12412412412 - 23.11.2023 10:54
        help_text=_("Consignment note"),
    )
    warehouse_item = models.ForeignKey(
        WarehouseItem,
        on_delete=models.CASCADE,
        related_name="arrivals",
        help_text=_("Product arrived"),
    )
    arrival_type = models.CharField(
        max_length=50,
        choices=ArrivalTypeChoices.choices,
        help_text=_("type of arrival"),
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
        db_table = "goods_arrival"
        verbose_name = _("Goods Arrival")
        verbose_name_plural = _("Goods Arrivals")

    def __str__(self):
        """
        Return a string representation of the Goods arrival model.

        :return: string representation of model
        """
        return (
            f"Arrival of {self.warehouse_item.product} - "
            f"Type: {self.get_arrival_type_display()}, Document: {self.document}"
        )
