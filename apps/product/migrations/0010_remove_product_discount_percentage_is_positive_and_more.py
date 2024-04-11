# Generated by Django 4.2.8 on 2024-03-04 14:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_alter_category_slug'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='product',
            name='discount_percentage_is_positive',
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0, message='Discount percentage cannot be less than 0.'), django.core.validators.MaxValueValidator(100, message='Discount percentage cannot be greater than 100.')]),
        ),
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='This field allows empty value', max_digits=3, null=True, verbose_name='Rating'),
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('rating__gt', 0), ('rating__lte', 5)), ('rating__isnull', True), _connector='OR'), name='rating_from_0_to_5_or_null', violation_error_message='Rating must be from 0 to 5 or null.'),
        ),
    ]
