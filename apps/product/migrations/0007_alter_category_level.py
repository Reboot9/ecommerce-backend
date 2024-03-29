# Generated by Django 4.2.8 on 2024-01-15 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_category_options_category_level_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='level',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Top Level'), (1, 'Medium Level'), (2, 'Lower Level')], default=0, help_text='Select the level of this category. Top Level is for main categories, Medium Level for subcategories, and Lower Level for the most specific categories.', verbose_name='Category Level'),
        ),
    ]
