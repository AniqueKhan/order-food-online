# Generated by Django 3.2.20 on 2023-08-17 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dishcategory',
            options={'verbose_name_plural': 'Dish Categories'},
        ),
        migrations.AddField(
            model_name='restaurant',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='restuarants/'),
        ),
    ]
