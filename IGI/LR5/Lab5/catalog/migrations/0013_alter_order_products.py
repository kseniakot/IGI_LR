# Generated by Django 5.0.4 on 2024-05-18 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_alter_order_total_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='catalog.productinstance'),
        ),
    ]
