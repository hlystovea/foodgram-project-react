from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers, validators

from api import serializers as srlz
from .models import Subscription
from .utils import get_limit

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
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class SubscriptionReadSerializer(CustomUserSerializer):
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


class SubscriptionWriteSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate_author(self, author):
        if self.context['request'].user == author:
            raise serializers.ValidationError(
                _('Вы пытаетесь подписаться на самого себя.')
            )
        return author

    class Meta:
        model = Subscription
        fields = '__all__'
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=['author', 'user'],
                message=_('Вы уже подписаны на этого автора.')
            ),
        ]
