# Generated by Django 4.2.8 on 2024-02-14 12:05

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_alter_order_order_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('city', models.CharField(max_length=250, verbose_name='City')),
                ('option', models.CharField(max_length=250, verbose_name='Delivery option')),
                ('street', models.CharField(blank=True, max_length=250, null=True, verbose_name='Street')),
                ('house', models.CharField(blank=True, max_length=50, null=True, verbose_name='House')),
                ('flat', models.CharField(blank=True, max_length=20, null=True, verbose_name='Flat')),
                ('floor', models.SmallIntegerField(blank=True, null=True, verbose_name='Floor')),
                ('entrance', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Entrance')),
                ('department', models.CharField(blank=True, max_length=250, null=True, verbose_name='Department')),
                ('time', models.DateField(blank=True, null=True, verbose_name='Delivery time')),
                ('declaration', models.CharField(blank=True, max_length=250, null=True, verbose_name='Declaration')),
            ],
            options={
                'verbose_name': 'Delivery',
                'verbose_name_plural': 'Deliveries',
                'db_table': 'deliveries',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='delivery',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='deliveries', to='order.delivery'),
            preserve_default=False,
        ),
    ]
