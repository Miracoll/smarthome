# Generated by Django 4.2.5 on 2023-10-07 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_control_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('whatsapp_number', models.CharField(max_length=20)),
            ],
        ),
    ]
