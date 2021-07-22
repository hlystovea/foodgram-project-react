from django.db.models import Q
from django_filters import BooleanFilter, CharFilter, FilterSet, NumberFilter

from .models import Ingredient, Recipe


class IngredientFilter(FilterSet):
    name = CharFilter(field_name='name', method='filter_name')

    def filter_name(self, queryset, name, value):
        return queryset.filter(
            Q(name__istartswith=value) | Q(name__icontains=value)
        )

    class Meta:
        model = Ingredient
        fields = ['name', ]


class RecipeFilter(FilterSet):
    tags = CharFilter(field_name='tags__slug', method='filter_tags')
    author = NumberFilter(field_name='author__id')
    is_favorited = BooleanFilter(field_name='is_favorited')
    is_in_shopping_cart = BooleanFilter(field_name='is_in_shopping_cart')

    def filter_tags(self, queryset, slug, tags):
        return queryset.filter(
            tags__slug__in=tags.split(',')
        ).distinct()

    class Meta:
        model = Recipe
        fields = ['author', 'is_favorited', 'is_in_shopping_cart', 'tags']
