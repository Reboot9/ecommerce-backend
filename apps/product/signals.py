"""
Module to define signals for the product app.
"""
from django.db.models.signals import pre_save, post_save, post_delete
from django.core.cache import cache
from django.dispatch import receiver
from django.utils.text import slugify

from apps.product.models import Category, Product


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


@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def clear_category_cache(sender, instance, **kwargs) -> None:
    """
    Signal receiver function to update category cache when a Category instance is saved or deleted.
    """
    cache_key_pattern = "category*"
    cache.delete_pattern(cache_key_pattern)


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def clear_product_cache(sender, instance, **kwargs) -> None:
    """
    Signal receiver function to clear product cache when a Product instance is saved or deleted.
    """
    cache_key_pattern = "product*"
    cache.delete_pattern(cache_key_pattern)
