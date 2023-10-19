from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Control


# @receiver(post_save, sender=Control) 
# def update_control(sender, instance, created, **kwargs):
# 	if not created:
		