from django_filters import BooleanFilter, CharFilter, FilterSet, NumberFilter

from .models import Ingredient, Recipe


class IngredientFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeFilter(FilterSet):
    tags = CharFilter(field_name='tags__slug', method='filter_tags')
    author = NumberFilter(field_name='author__id')
    is_favorited = BooleanFilter(field_name='is_favorited')
    is_in_shopping_cart = BooleanFilter(field_name='is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ['author', 'is_favorited', 'is_in_shopping_cart', 'tags']

    def filter_tags(self, queryset, name, value):
        values = self.data.getlist('tags')
        lookup = f'{name}__in'
        return queryset.filter(**{lookup: values}).distinct()
