from django.contrib.auth import get_user_model
from swings.models import Swing
from rest_framework import serializers
from django.db.models import Max

class UserSerializer(serializers.ModelSerializer):
    #gender = serializers.CharField(source='get_gender_display') #display gender as string
    top_speed = serializers.SerializerMethodField()
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password', 'is_staff', 'is_active', 'is_superuser', 'date_created', 'profile_picture', 'age', 'gender', 'height', 'handicap','lefty', 'top_speed']
        extra_kwargs = {
            'date_created': {'read_only': True},
            'password': {'write_only': True},
            'is_active': {'default': True},
        }

    def update(self, instance, validated_data):
        if ('password' in validated_data):
            raise serializers.ValidationError("Use API endpoint /users/set_password/ to update passwords.")
        elif ('is_staff' in validated_data):
            raise serializers.ValidationError("Contact the database administrator to update is_staff")
        elif ('is_superuser' in validated_data):
            raise serializers.ValidationError("Contact the database administrator to update is_superuser")
        return super().update(instance, validated_data)

    def get_top_speed(self, user):
        swings = Swing.objects.filter(user=user)
        top_speed = swings.aggregate(Max('speed'))
        return top_speed.get('speed__max')

class UserProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['profile_picture']


