# Generated by Django 3.2.16 on 2022-10-18 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studio', '0006_remove_user_consent'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='day_add',
            field=models.DateField(blank=True, null=True),
        ),
    ]
