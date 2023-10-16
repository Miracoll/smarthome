from rest_framework import serializers
from .models import Control, Config

# class ControlSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Control
#         fields = '__all__'

class LEDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Control
        fields = ['name','status','acknowledge_response','ref']

class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.acknowledge_response = validated_data.get('acknowledge_response', instance.acknowledge_response)
        instance.acknowledge_request = validated_data.get('acknowledge_request', instance.acknowledge_request)
        instance.connection_status = validated_data.get('connection_status', instance.connection_status)
        instance.whatsapp_number = validated_data.get('whatsapp_number', instance.whatsapp_number)
        instance.save()
        return instance