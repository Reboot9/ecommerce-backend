# Generated by Django 4.2.8 on 2024-02-29 15:14

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_alter_category_slug'),
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsignmentNote',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('number', models.CharField(help_text='Consignment note number', max_length=250, unique=True)),
                ('consignment_date', models.DateField(help_text='The date of the consignment note document.')),
            ],
            options={
                'verbose_name': 'Consignment Note',
                'verbose_name_plural': 'Consignment Notes',
                'db_table': 'consignment_note',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('transaction_type', models.CharField(choices=[('arrival', 'Arrival'), ('return', 'Return'), ('inventory', 'Inventory'), ('order', 'Order'), ('write-off', 'Write-off')], help_text='Type of transaction', max_length=50)),
                ('quantity', models.PositiveIntegerField(default=0, help_text='Quantity of the product', validators=[django.core.validators.MinLengthValidator(1)])),
                ('comment', models.TextField(blank=True, help_text='Additional comments', max_length=2000, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('consignment_note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.consignmentnote')),
                ('product', models.ForeignKey(help_text='Product related to this transaction', on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='product.product')),
            ],
            options={
                'verbose_name': 'Goods Transaction',
                'verbose_name_plural': 'Goods Transaction',
                'db_table': 'goods_transaction',
                'ordering': ['-created_at'],
            },
        ),
        migrations.RemoveField(
            model_name='goodsconsumption',
            name='warehouse_item',
        ),
        migrations.RemoveField(
            model_name='warehouseitem',
            name='product',
        ),
        migrations.RemoveField(
            model_name='reserve',
            name='warehouse_item',
        ),
        migrations.RemoveField(
            model_name='warehouse',
            name='product_name',
        ),
        migrations.AddField(
            model_name='reserve',
            name='quantity',
            field=models.PositiveIntegerField(default=0, help_text='Quantity of the product', validators=[django.core.validators.MinLengthValidator(1)]),
        ),
        migrations.AddField(
            model_name='reserve',
            name='reserved_item',
            field=models.ForeignKey(default='', help_text='Product reserved', on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='product.product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='warehouse',
            name='product',
            field=models.ForeignKey(default='', help_text='The product stored in warehouse', on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='Product'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='GoodsArrival',
        ),
        migrations.DeleteModel(
            name='GoodsConsumption',
        ),
        migrations.DeleteModel(
            name='WarehouseItem',
        ),
        migrations.AddIndex(
            model_name='consignmentnote',
            index=models.Index(fields=['consignment_date'], name='idx_consignment_note_date'),
        ),
        migrations.AlterUniqueTogether(
            name='consignmentnote',
            unique_together={('number', 'consignment_date')},
        ),
    ]