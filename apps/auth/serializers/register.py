from django.core.mail import send_mail
from rest_framework import serializers
from apps.user.serializers import UserSerializer
from apps.user.models import User


class RegisterSerializer(UserSerializer):
    password = serializers.CharField(max_length=128,
                                     min_length=8, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email',
                  'username',
                  'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
