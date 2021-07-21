from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth import get_user_model
from drf_base64.serializers import ModelSerializer
from rest_framework import serializers, validators
from rest_framework.fields import ImageField

from users.serializers import CustomUserSerializer
from . import models

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Ingredient


class QuantitySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id', read_only=True)
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True,
    )

    class Meta:
        fields = ['id', 'name', 'measurement_unit', 'amount']
        model = models.Quantity


class QuantityWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=models.Ingredient.objects.all()
    )

    class Meta:
        fields = ['id', 'amount']
        model = models.Quantity


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Tag


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = QuantitySerializer(many=True, read_only=True)
    is_favorited = serializers.BooleanField(default=False)
    is_in_shopping_cart = serializers.BooleanField(default=False)

    class Meta:
        fields = '__all__'
        model = models.Recipe


class RecipeWriteSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    ingredients = QuantityWriteSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        fields = '__all__'
        model = models.Recipe

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = models.Recipe.objects.create(**validated_data)
        for ingredient in ingredients_data:
            ingredient, created = models.Quantity.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount'],
            )
        for tag in tags_data:
            recipe.tags.add(tag)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')

        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time,
        )
        instance.tags.set(tags_data)

        models.Quantity.objects.filter(recipe=instance).delete()

        for ingredient in ingredients_data:
            ingredient, created = models.Quantity.objects.get_or_create(
                recipe=instance,
                ingredient=ingredient['id'],
                amount=ingredient['amount'],
            )

        return instance


class SubscriptionRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = models.Recipe


class SubscriptionSerializer(CustomUserSerializer):
    recipes = SubscriptionRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.IntegerField(read_only=True)

    class Meta(CustomUserSerializer.Meta):
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        model = User
