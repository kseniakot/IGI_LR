# Generated by Django 5.0.4 on 2024-05-17 16:24

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_alter_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular order across whole shop', primary_key=True, serialize=False),
        ),
    ]
