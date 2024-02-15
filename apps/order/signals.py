"""
Module: order_signals.

This module contains Django signals related to the 'Order' model in the 'order' app.
"""

from django.db.models import Max
from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.order.models.order import Order


@receiver(pre_save, sender=Order)
def update_order_number(sender, instance, **kwargs):
    """Signal handler to update the order number before saving an Order instance."""
    if not instance.order_number:
        max_value = Order.objects.aggregate(order_number_max=Max("order_number"))[
            "order_number_max"
        ]
        instance.order_number = max_value + 1 if max_value is not None else 1
