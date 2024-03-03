"""
Module defines Warehouse model for warehouse app.
"""
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseDate, BaseID
from apps.product.models import Product
from apps.warehouse.models.reserve import Reserve


class Warehouse(BaseID, BaseDate):
    """
    Represents a warehouse item with its balance and reserves.

    This model stores information about a specific product in the warehouse,
    including its total balance, reserved quantity, and availability for orders.
    """

    product = models.ForeignKey(  # 1:1 field?
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
        help_text=_("The product stored in warehouse"),
    )
    total_balance = models.IntegerField(
        default=0,
        verbose_name=_("Total balance"),
        help_text=_("The quantity of the product in the warehouse"),
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        db_table = "warehouse"
        verbose_name = _("Warehouse")
        verbose_name_plural = _("Warehouses")

    @property
    def reserve(self):
        """
        Calculates and returns the quantity of the product reserved from the warehouse.
        """
        return (
            Reserve.objects.filter(reserved_item=self.product, is_active=True).aggregate(
                Sum("quantity")
            )["quantity__sum"]
            or 0
        )

    @property
    def free_balance(self):
        """
        Calculates and returns the quantity of the product available for order.

        Note: Raises a validation error if total_balance is less than the reserve.
        """
        return self.total_balance - self.reserve

    def __str__(self) -> str:
        """
        Return a string representation of the Warehouse model.

        :return: string representation of model
        """
        return (
            f"{self.product.name} - Total: {self.total_balance}, Reserve: {self.reserve},"
            f" Free: {self.free_balance}"
        )

    def clean(self):
        """
        Override default method to enforce custom validation rules.
        """
        super().clean()

        # if self.total_balance < self.reserve:
        #     raise ValidationError(_("Total balance cannot be less than the reserve"))
