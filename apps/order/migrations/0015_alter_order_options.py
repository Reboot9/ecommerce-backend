# Generated by Django 4.2.11 on 2024-03-22 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_orderitem_discount_percentage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-order_number'], 'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
    ]
