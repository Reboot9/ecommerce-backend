"""
Module: order.py.

This module defines the Order model for the order app.
"""
from decimal import Decimal, ROUND_HALF_UP

from django.db import models
from django.db.models import Sum, ExpressionWrapper, F, DecimalField

from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseDate, BaseID
from apps.order.models.delivery import Delivery
from apps.order.utils import phone_validator


class Order(BaseID, BaseDate):
    """Model representing an order."""

    class OrderStatusChoices(models.TextChoices):
        """Enum for order status."""

        NEW = "N", _("NEW")  # The order was successfully created in the system.
        PROCESSING = "P", _("Processing")  # The order has been accepted and is in
        # the process of being prepared for shipment.
        SENT = "S", _("Sent")  # The order is in the process of being transported
        # from the sender to the recipient.
        DELIVERED = "D", _("Delivered")  # The order has been successfully delivered
        # to the recipient.
        EXECUTED = "E", _("Executed")  # The order completed
        CANCELED = "C", _("Canceled")  # The order cancelled
        RETURNED = "R", _("Returned")  # The order was returned to the sender for some reason
        ISSUE = "I", _("Issue")  # There was a problem with the order

    status = models.CharField(
        verbose_name=_("Status"),
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.NEW,
    )
    first_name = models.CharField(
        max_length=250,
        verbose_name=_("First name"),
    )
    last_name = models.CharField(max_length=250, verbose_name=_("Last name"))
    phone = models.CharField(
        max_length=17,  # +38(050)111-11-11
        verbose_name=_("Mobile phone"),
        validators=[phone_validator],
    )
    email = models.EmailField(max_length=250, verbose_name=_("Email"))
    comment = models.CharField(
        max_length=255,
        verbose_name=_("Comment"),
        null=True,
        blank=True,
    )
    is_paid = models.BooleanField(
        verbose_name=_("Paid"),
        default=False,
    )
    order_number = models.IntegerField(unique=True, editable=False)
    delivery = models.ForeignKey(
        to=Delivery,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deliveries",
    )

    class Meta:
        db_table = "orders"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-order_number"]

    def __str__(self):
        """This method is automatically called when you use the str() function.

        Or when the object needs to be represented as a string
        """
        return (
            f"Order №{self.order_number}, {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}, "
            f"status-{self.get_status_display()}, paid-{self.is_paid}"
        )

    @property
    def total_order_price(self):
        """Calculate the total cost of items in the order."""
        total_price = self.items.aggregate(
            total_price=Sum(
                ExpressionWrapper(
                    F("quantity") * F("price") * ((100 - F("discount_percentage")) / 100),
                    output_field=DecimalField(),
                )
            )
        )["total_price"] or Decimal("0")
        return Decimal(total_price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
