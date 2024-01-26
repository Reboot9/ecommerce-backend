"""
Module to define signals for the product app.
"""
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from apps.product.models import Category


@receiver(pre_save, sender=Category)
def generate_slug(sender, instance, **kwargs) -> None:
    """
    Signal receiver function to automatically generate a slug for a Category before saving.

    If the slug is not provided, it generates a slug based on the 'name' field
    using the slugify function.

    :param sender: The model class that sends the signal.
    :param instance: The actual instance being saved.
    :param kwargs: Additional keyword arguments.
    :return: None
    """
    if not instance.slug:
        instance.slug = slugify(instance.name)
