# Generated by Django 4.2.8 on 2024-02-26 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_alter_delivery_option'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='entrance',
            field=models.CharField(blank=True, help_text='This field accepts text. Example: Entrance to a toy store', null=True, verbose_name='Entrance'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='flat',
            field=models.CharField(blank=True, help_text='This field accepts text. Example: 30/1', max_length=20, null=True, verbose_name='Flat'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='house',
            field=models.CharField(blank=True, help_text='This field accepts text. Example: 20B', max_length=50, null=True, verbose_name='House'),
        ),
    ]