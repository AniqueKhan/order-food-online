# Generated by Django 3.2.20 on 2023-08-21 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0010_dish_on_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='on_sale_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
