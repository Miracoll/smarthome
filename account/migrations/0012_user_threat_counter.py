# Generated by Django 4.2.5 on 2023-10-14 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_user_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='threat_counter',
            field=models.IntegerField(default=0),
        ),
    ]
