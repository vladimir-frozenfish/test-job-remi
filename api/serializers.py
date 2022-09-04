from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from shop.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = (
                "email",
                "id",
                "username",
                "first_name",
                "last_name",
                "password"
            )
        model = User

    def create(self, validated_data):
        """создание хэшируемого пароля"""
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)