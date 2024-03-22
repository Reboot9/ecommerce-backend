"""
Utility functions for Order app.
"""
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

phone_validator = RegexValidator(
    regex=r"^\+\d{2}\(\d{3}\)\d{3}-\d{2}-\d{2}$",
    message=_(
        "Phone number must be entered in the format: '+38(050)111-11-11'. Up to 17 digits allowed."
    ),
)


def create_reserve(order_instance, item):
    """
    Create a reserve for the given order item.
    """
    from apps.warehouse.models import Reserve

    reserve, _ = Reserve.objects.get_or_create(
        order=order_instance, reserved_item=item.product, quantity=item.quantity
    )
    reserve.save()


def create_or_update_transaction(order_instance, item, *, transaction_type):
    """
    Create or update a transaction for the given order item.
    """
    from apps.warehouse.models import Reserve, Transaction
    from apps.order.models.order import Order

    is_active = order_instance.status not in [
        Order.OrderStatusChoices.NEW,
        Order.OrderStatusChoices.PROCESSING,
        Order.OrderStatusChoices.CANCELED,
        Order.OrderStatusChoices.ISSUE,
    ]
    print(is_active)
    transaction, _ = Transaction.objects.get_or_create(
        product=item.product,
        order_item=item,
        quantity=item.quantity,
    )
    transaction.transaction_type = transaction_type
    transaction.is_active = is_active
    transaction.save()

    related_reserve = Reserve.objects.get(order=order_instance, reserved_item=item.product)

    # Update is_active based on the conditions
    if order_instance.status in [
        Order.OrderStatusChoices.CANCELED,
        Order.OrderStatusChoices.ISSUE,
    ]:
        related_reserve.is_active = False
    elif is_active:
        related_reserve.is_active = False
    else:
        related_reserve.is_active = True

    related_reserve.save()
