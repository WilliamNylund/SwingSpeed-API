from django.contrib.auth import get_user_model
from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password', 'is_staff', 'is_active', 'is_superuser', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}, 'is_active': {'default': True}}



