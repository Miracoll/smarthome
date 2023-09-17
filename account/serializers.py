from rest_framework import serializers
from .models import LED

class LEDSerializer(serializers.ModelSerializer):
    class Meta:
        model = LED
        fields = '__all__'