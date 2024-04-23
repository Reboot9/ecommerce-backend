"""
Django signals related to the warehouse app.
"""
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.product.models.product import Product
from apps.warehouse.models import Transaction
from apps.warehouse.models.warehouse import Warehouse


@receiver(post_save, sender=Product)
def ensure_warehouse_for_product(sender, instance, created, **kwargs):
    """
    Signal handler to ensure that each product has a corresponding warehouse instance.
    """
    warehouse_item, _ = Warehouse.objects.get_or_create(product=instance)


@receiver(post_save, sender=Transaction)
def update_total_balance(sender, instance, created, **kwargs):
    """
    Signal to update the total balance of the warehouse after an arrival transaction is created.
    """
    if (
        instance.transaction_type == Transaction.TransactionTypeChoices.ARRIVAL
        and instance.consignment_note
    ):
        product_id = instance.product_id
        quantity = instance.quantity
        Warehouse.objects.filter(product_id=product_id).update(
            total_balance=F("total_balance") + quantity
        )
