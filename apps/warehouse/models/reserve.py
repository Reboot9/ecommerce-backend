"""
Module defines Reserve model for warehouse app.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseDate, BaseID
from apps.order.models.order import Order
from apps.warehouse.models.warehouse_item import WarehouseItem


class Reserve(BaseID, BaseDate):
    """
    Represents the reservation of products for orders.
    """

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, help_text=_("The order for which the product is reserved")
    )
    warehouse_item = models.ForeignKey(  # m:m
        WarehouseItem,
        on_delete=models.CASCADE,
        related_name="reservations",
        help_text=_("Product reserved"),
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        db_table = "reserve"
        verbose_name = _("Reserve")
        verbose_name_plural = _("Reserves")

    def __str__(self):
        """
        Return a string representation of the Reserve model.

        :return: string representation of model
        """
        # warehouse_items_str = ', '.join(str(item) for item in self.warehouse_item.all())
        return (
            f"Reserve for Order №{self.order.order_number}, "
            f"{self.order.created_at.strftime('%Y-%m-%d %H:%M:%S')}, Product: "
            f"{self.warehouse_item.product}; Quantity: {self.warehouse_item.quantity}"
        )
