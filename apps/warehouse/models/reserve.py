"""
Module defines Reserve model for warehouse app.
"""
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseDate, BaseID
from apps.order.models.order import Order
from apps.product.models import Product


class Reserve(BaseID, BaseDate):
    """
    Represents the reservation of products for orders.
    """

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, help_text=_("The order for which the product is reserved")
    )
    reserved_item = models.ForeignKey(  # m:m
        Product,
        on_delete=models.CASCADE,
        related_name="reservations",
        help_text=_("Product reserved"),
    )
    quantity = models.PositiveIntegerField(
        default=0,
        help_text=_("Quantity of the product"),
        validators=[validators.MinLengthValidator(1)],
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
            f"{self.reserved_item}; Quantity: {self.quantity}"
        )

    def clean(self):
        """
        Override default method to enforce custom validation rules.
        """
        super().clean()

        if self.quantity < 1:
            raise ValidationError(_("Quantity must be at least 1."))
