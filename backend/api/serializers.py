from rest_framework import serializers

from . import models


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Ingredient


class QuantitySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Quantity


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Tag


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Recipe
