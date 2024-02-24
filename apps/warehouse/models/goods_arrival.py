"""
Module defines Goods arrival model for warehouse app.
"""
from django.contrib.contenttypes.fields import GenericRelation
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

    warehouse_items = GenericRelation(WarehouseItem)
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
        warehouse_items_str = ", ".join(str(item) for item in self.warehouse_items.all())
        return (
            f"Arrival Type: {self.arrival_type}, Document: {self.consignmentnote}, "
            f"Warehouse Items: [{warehouse_items_str}]"
        )
