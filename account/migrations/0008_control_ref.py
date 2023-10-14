# Generated by Django 4.2.5 on 2023-10-13 13:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='control',
            name='ref',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]