"""
Django signals related to the order app.
"""
from django.db.models import Max
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from apps.order.models.order import Order
from apps.order.models.order_item import OrderItem
from apps.order.utils import create_reserve, create_or_update_transaction


@receiver(pre_save, sender=Order)
def update_order_number(sender, instance, **kwargs):
    """Signal handler to update the order number before saving an Order instance."""
    if not instance.order_number:
        max_value = Order.objects.aggregate(order_number_max=Max("order_number"))[
            "order_number_max"
        ]
        instance.order_number = max_value + 1 if max_value is not None else 1


@receiver(post_save, sender=Order)
def manage_order_items_transactions(sender, instance, created, **kwargs):
    """
    Signal to create reserves or update transactions based on the order status.
    """
    from apps.warehouse.models import Transaction

    order_status = instance.status

    # Define the mapping of order statuses to transaction types
    status_transaction_mapping = {
        Order.OrderStatusChoices.NEW: Transaction.TransactionTypeChoices.ORDER,
        Order.OrderStatusChoices.PROCESSING: Transaction.TransactionTypeChoices.ORDER,
        Order.OrderStatusChoices.SENT: Transaction.TransactionTypeChoices.ORDER,
        Order.OrderStatusChoices.DELIVERED: Transaction.TransactionTypeChoices.ORDER,
        Order.OrderStatusChoices.EXECUTED: Transaction.TransactionTypeChoices.ORDER,
        Order.OrderStatusChoices.CANCELED: Transaction.TransactionTypeChoices.RETURN,
        Order.OrderStatusChoices.RETURNED: Transaction.TransactionTypeChoices.RETURN,
        Order.OrderStatusChoices.ISSUE: Transaction.TransactionTypeChoices.RETURN,
    }

    # Get the transaction type based on the order status
    transaction_type = status_transaction_mapping.get(order_status)

    # Create or update transaction based on the order status
    if transaction_type:
        for item in instance.items.all():
            if order_status in [Order.OrderStatusChoices.NEW, Order.OrderStatusChoices.PROCESSING]:
                create_reserve(instance, item)
            create_or_update_transaction(instance, item, transaction_type=transaction_type)


@receiver(post_save, sender=OrderItem)
def create_reserves_for_order_item(sender, instance, created, **kwargs):
    """
    Utility signal to create model instances when creating an OrderItem.
    """
    from apps.warehouse.models import Reserve, Transaction

    if created:
        order = instance.order
        order_status = order.status
        if order_status in [
            Order.OrderStatusChoices.NEW,
            Order.OrderStatusChoices.PROCESSING,
        ]:
            create_reserve(order, instance)
        else:
            # Determine transaction type and is_active flag based on order status
            is_active = order_status not in [
                Order.OrderStatusChoices.EXECUTED,
                Order.OrderStatusChoices.ISSUE,
            ]
            transaction_type = (
                Transaction.TransactionTypeChoices.ORDER
                if order_status
                not in (Order.OrderStatusChoices.ISSUE, Order.OrderStatusChoices.EXECUTED)
                else Transaction.TransactionTypeChoices.RETURN
            )

            # Create transaction for the order item
            Transaction.objects.create(
                product=instance.product,
                order_item=instance,
                quantity=instance.quantity,
                transaction_type=transaction_type,
                is_active=is_active,
            )

            # Deactivate related reserve
            Reserve.objects.get_or_create(
                order=order,
                reserved_item=instance.product,
            ).update(is_active=False)
    else:
        # Update related reserve and transaction
        order = instance.order
        reserve = Reserve.objects.get(
            order=order,
            reserved_item=instance.product,
        )

        transaction, created = Transaction.objects.get_or_create(
            order_item=instance,
            transaction_type=Transaction.TransactionTypeChoices.ORDER,
            defaults={
                "product": instance.product,
                "quantity": instance.quantity,
                "is_active": True,
            },
        )

        reserve.quantity = instance.quantity
        reserve.save()

        if not created:
            transaction.quantity = instance.quantity
            transaction.save()
