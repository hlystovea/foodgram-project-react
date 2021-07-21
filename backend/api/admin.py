from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from . import models

User = get_user_model()


class MixinAdmin(admin.ModelAdmin):
    empty_value_display = _('-пусто-')


@admin.register(models.Ingredient)
class IngredientAdmin(MixinAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name', )
    list_filter = ('measurement_unit', )


class QuantityInline(admin.TabularInline):
    model = models.Quantity
    autocomplete_fields = ('ingredient', )
    min_num = 1
    extra = 0


@admin.register(models.Recipe)
class RecipeAdmin(MixinAdmin):
    list_display = ('id', 'name', 'author', 'cooking_time')
    search_fields = ('name', 'author', 'tags')
    list_filter = ('tags', )
    inlines = [
        QuantityInline,
    ]


@admin.register(models.Tag)
class TagAdmin(MixinAdmin):
    list_display = ('id', 'name', 'slug', 'color')
    search_fields = ('name', 'slug')
    list_filter = ('color', )
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('name', 'slug', 'color')


@admin.register(models.Subscription)
class SubscriptionAdmin(MixinAdmin):
    list_display = ('id', 'user', 'author')
    search_fields = ('user', 'author')
    autocomplete_fields = ('user', 'author')


@admin.register(models.Favorite)
class FavoriteAdmin(MixinAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    autocomplete_fields = ('user', 'recipe')
