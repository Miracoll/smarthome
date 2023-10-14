from rest_framework import serializers
from .models import Control, Config

class LEDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Control
        fields = '__all__'

class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = '__all__'