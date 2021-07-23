from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name', 'is_subscribed')


class CustomUserCreateSerializer(UserCreateSerializer):
    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True
    )

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
