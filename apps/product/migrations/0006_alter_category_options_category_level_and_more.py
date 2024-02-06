# Generated by Django 4.2.8 on 2024-01-12 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_rename_product_charactetistic_productcharacteristics_product_characteristic_and_more')
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['level', 'name'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='category',
            name='level',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='product.category'),
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='', max_length=256, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=256, verbose_name='Name'),
        ),
    ]
