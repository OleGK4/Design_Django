# Generated by Django 4.1.2 on 2022-10-18 10:22

import django.core.validators
from django.db import migrations, models
import studio.models


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0007_order_day_add'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='photo_file',
            field=models.ImageField(max_length=200, null=True, upload_to=studio.models.get_name_file, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])]),
        ),
    ]
