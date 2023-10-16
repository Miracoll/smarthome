from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    password_reset = models.BooleanField(default=False)
    image = models.ImageField(default='passport.jpg', upload_to='passport')
    role = models.CharField(max_length=255, blank=True, null=True)
    threat_counter = models.IntegerField(default=0)
    disable_reason = models.TextField(max_length=200, blank=True, null=True)
    ip_address = models.CharField(max_length=20, blank=True, null=True)

class Control(models.Model):
    name = models.CharField(max_length=100)
    keyword = models.CharField(max_length=100)
    level = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    acknowledge_response = models.BooleanField(default=False)
    connection_status = models.BooleanField(default=False)
    image = models.ImageField(upload_to='control', default='control.png', blank=True, null=True)
    user = models.ForeignKey(User, models.CASCADE)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
class Config(models.Model):
    whatsapp_number = models.CharField(max_length=20)
    acknowledge_request = models.BooleanField(default=True)
    acknowledge_response = models.BooleanField(default=False)
    connection_status = models.BooleanField(default=False)

class History(models.Model):
    action = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    ip_address = models.CharField(max_length=20)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.user
