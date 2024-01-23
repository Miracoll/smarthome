# Generated by Django 4.2.5 on 2023-10-20 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='acknowledge_request',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='acknowledge_response',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='connection_status',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='whatsapp_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
