"""
Module defines Goods arrival model for warehouse app.
"""
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseDate, BaseID
from apps.product.models import Product
from apps.warehouse.models.consignment_note import ConsignmentNote


class Transaction(BaseID, BaseDate):
    """
    Represents the arrival of products to the warehouse.
    """

    class TransactionTypeChoices(models.TextChoices):
        """Enum for transaction types."""

        # Types for arrival
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
        # Types for consumption
        ORDER = (
            "order",
            _("Order"),
        )
        WRITE_OFF = (
            "write-off",
            _("Write-off"),
        )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="transactions",
        help_text=_("Product related to this transaction"),
    )
    consignment_note = models.ForeignKey(ConsignmentNote, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=50,
        choices=TransactionTypeChoices.choices,
        help_text=_("Type of transaction"),
    )
    quantity = models.PositiveIntegerField(
        default=0,
        help_text=_("Quantity of the product"),
        validators=[validators.MinLengthValidator(1)],
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
        db_table = "goods_transaction"
        verbose_name = _("Goods Transaction")
        verbose_name_plural = _("Goods Transaction")

    def __str__(self):
        """
        Return a string representation of the Goods arrival model.

        :return: string representation of model
        """
        # warehouse_items_str = ", ".join(str(item) for item in self.warehouse_items.all())
        return (
            f"Transaction Type: {self.transaction_type}, Document: {self.consignmentnote}, "
            # f"Warehouse Items: [{warehouse_items_str}]"
        )

    @property
    def is_arrival(self):
        """Check if the transaction is an arrival."""
        return self.transaction_type in [
            self.TransactionTypeChoices.ARRIVAL,
            self.TransactionTypeChoices.RETURN,
            self.TransactionTypeChoices.INVENTORY,
        ]

    def clean(self):
        """
        Override default method to enforce custom validation rules.
        """
        super().clean()

        if self.quantity < 1:
            raise ValidationError(_("Quantity must be at least 1."))
