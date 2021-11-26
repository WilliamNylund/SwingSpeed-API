from .models import Swing
from rest_framework import serializers

class SwingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Swing
        fields = ['id', 'user', 'speed', 'date_created', 'is_active', 'note']
        extra_kwargs = {
            'date_created': {'read_only': True},
            'is_active': {'default': True},
        }

class SwingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Swing
        fields = ['note']