# Generated by Django 4.2.5 on 2023-10-16 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_config_acknowledge_response_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='acknowledge_request',
            field=models.BooleanField(default=False),
        ),
    ]
