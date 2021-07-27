from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
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
    list_editable = ('name', 'measurement_unit')


class QuantityInline(admin.TabularInline):
    model = models.Quantity
    autocomplete_fields = ('ingredient', )
    min_num = 1
    extra = 0


@admin.register(models.Recipe)
class RecipeAdmin(MixinAdmin):
    list_display = ('id', 'name', 'get_user', 'cooking_time', 'get_pub_date',
                    'get_change_date', 'number_in_favorites', 'image_tag')
    search_fields = ('name', 'author', 'tags')
    readonly_fields = ('image_tag',)
    list_filter = ('tags', )
    inlines = [QuantityInline]

    @admin.display(description=_('Автор'))
    def get_user(self, obj):
        user = obj.author
        url = (
            reverse('admin:users_customuser_changelist')
            + '?'
            + urlencode({'id': f'{user.id}'})
        )
        return format_html('<a href="{}">{}</a>', url, user)

    @admin.display(description=_('Дата публикации'))
    def get_pub_date(self, obj):
        return obj.pub_date.strftime('%Y-%m-%d %H:%M')

    @admin.display(description=_('Дата изменения'))
    def get_change_date(self, obj):
        return obj.change_date.strftime('%Y-%m-%d %H:%M')

    @admin.display(description=_('Кол-во добавлений в избранное'))
    def number_in_favorites(self, obj):
        count = obj.additions.count()
        url = (
            reverse('admin:api_favorite_changelist')
            + '?'
            + urlencode({'recipe__id': f'{obj.id}'})
        )
        return format_html('<a href="{}">{} чел.</a>', url, count)

    @admin.display(description=_('Картинка'))
    def image_tag(self, instance):
        if instance.image:
            return format_html(
                '<img src="{0}" style="max-height: 50px"/>',
                instance.image.url,
            )
        return None


@admin.register(models.Tag)
class TagAdmin(MixinAdmin):
    list_display = ('id', 'name', 'slug', 'color')
    search_fields = ('name', 'slug')
    list_filter = ('color', )
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('name', 'slug', 'color')


@admin.register(models.Favorite)
class FavoriteAdmin(MixinAdmin):
    list_display = ('id', 'get_user', 'get_recipe')
    search_fields = ('user', 'recipe')
    autocomplete_fields = ('user', 'recipe')

    @admin.display(description=_('Пользователь'))
    def get_user(self, obj):
        user = obj.user
        url = (
            reverse('admin:users_customuser_changelist')
            + '?'
            + urlencode({'id': f'{user.id}'})
        )
        return format_html('<a href="{}">{}</a>', url, user)

    @admin.display(description=_('Рецепт'))
    def get_recipe(self, obj):
        recipe = obj.recipe
        url = (
            reverse('admin:api_recipe_changelist')
            + '?'
            + urlencode({'id': f'{recipe.id}'})
        )
        return format_html('<a href="{}">{}</a>', url, recipe)


@admin.register(models.Purchase)
class PurchaseAdmin(MixinAdmin):
    list_display = ('id', 'get_user', 'get_recipe')
    search_fields = ('user', 'recipe')
    autocomplete_fields = ('user', 'recipe')

    @admin.display(description=_('Пользователь'))
    def get_user(self, obj):
        user = obj.user
        url = (
            reverse('admin:users_customuser_changelist')
            + '?'
            + urlencode({'id': f'{user.id}'})
        )
        return format_html('<a href="{}">{}</a>', url, user)

    @admin.display(description=_('Рецепт'))
    def get_recipe(self, obj):
        recipe = obj.recipe
        url = (
            reverse('admin:api_recipe_changelist')
            + '?'
            + urlencode({'id': f'{recipe.id}'})
        )
        return format_html('<a href="{}">{}</a>', url, recipe)
