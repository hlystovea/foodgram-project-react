from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

User = get_user_model()


from .utils import get_limit
from api import serializers as srlz


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
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class SubscriptionSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(read_only=True)

    class Meta(CustomUserSerializer.Meta):
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        model = User

    def get_recipes(self, obj):
        serializer = srlz.RecipeLiteSerializer(obj.recipes, many=True)
        request = self.context['request']
        limit = get_limit(request)
        return serializer.data[:limit]
