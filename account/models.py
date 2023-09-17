from django.db import models
from django.utils import timezone

# Create your models here.

class LED(models.Model):
    name = models.CharField(max_length=100)
    keyword = models.CharField(max_length=100)
    status = models.BooleanField()
    created = models.DateTimeField(default=timezone.now)