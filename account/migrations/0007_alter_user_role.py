# Generated by Django 4.2.5 on 2023-10-07 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_config'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
