# Generated by Django 4.2.8 on 2024-01-25 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Comment'),
        ),
    ]
