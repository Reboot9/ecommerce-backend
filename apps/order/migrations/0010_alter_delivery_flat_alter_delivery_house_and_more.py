# Generated by Django 4.2.8 on 2024-02-20 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_alter_delivery_option_alter_order_delivery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='flat',
            field=models.CharField(blank=True, help_text='This field can take text. Example: 30/1', max_length=20, null=True, verbose_name='Flat'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='house',
            field=models.CharField(blank=True, help_text='This field can take text. Example: 20B', max_length=50, null=True, verbose_name='House'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='option',
            field=models.CharField(choices=[('D', 'Delivery'), ('С', 'Courier')], default='С', max_length=250, verbose_name='Delivery option'),
        ),
    ]
