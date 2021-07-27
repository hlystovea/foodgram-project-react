from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import fields

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name=_('Единица измерения'),
        max_length=200,
    )

    class Meta:
        app_label = 'api'
        ordering = ('name', )
        verbose_name = _('Ингредиент')
        verbose_name_plural = _('Ингредиенты')

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Quantity(models.Model):
    ingredient = models.ForeignKey(
        to=Ingredient,
        verbose_name=_('Ингредиент'),
        on_delete=models.PROTECT,
    )
    recipe = models.ForeignKey(
        to='Recipe',
        verbose_name=_('Рецепт'),
        on_delete=models.CASCADE,
        related_name='ingredients',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name=_('Количество'),
        validators=[
            # здесь использую валидацию только по "верху", т.к. поле Positive
            validators.MaxValueValidator(
                99999,
                message='Слишком много, проверьте единицы измерения',
            ),
        ]
    )

    class Meta:
        app_label = 'api'
        ordering = ('ingredient', )
        verbose_name = _('Количество ингредиента')
        verbose_name_plural = _('Количества ингредиентов')

    def __str__(self):
        name = self.ingredient.name
        amount = self.amount
        measurement_unit = self.ingredient.measurement_unit
        return f'{name}: {amount} {measurement_unit}'


class Tag(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
        unique=True,
    )
    color = fields.ColorField(
        verbose_name=_('Цвет'),
        default='#FF0000',
    )
    slug = models.SlugField(
        verbose_name=_('Слаг'),
        max_length=200,
        unique=True,
    )
    order = models.PositiveSmallIntegerField(
        verbose_name=_('Порядок вывода'),
    )

    class Meta:
        app_label = 'api'
        ordering = ('order', 'name')
        verbose_name = _('Тег')
        verbose_name_plural = _('Теги')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        to=User,
        verbose_name=_('Автор'),
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    image = models.ImageField(
        verbose_name=_('Изображение'),
        upload_to='recipes/',
    )
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=200,
        unique=True,
    )
    text = models.TextField(
        verbose_name=_('Рецепт'),
    )
    pub_date = models.DateTimeField(
        verbose_name=_('Дата публикации'),
        auto_now_add=True,
    )
    change_date = models.DateTimeField(
        verbose_name=_('Дата изменения'),
        auto_now=True,
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name=_('Время приготовления, мин'),
        validators=[
            validators.MinValueValidator(
                1,
                message=_('Время не может быть меньше 1 минуты'),
            ),
            validators.MaxValueValidator(
                1000,
                message=_('Слишком долго, укажите время в минутах'),
            ),
        ]
    )
    tags = models.ManyToManyField(
        to=Tag,
        verbose_name=_('Теги'),
        related_name='recipes',
    )

    class Meta:
        app_label = 'api'
        ordering = ('-pub_date', )
        verbose_name = _('Рецепт')
        verbose_name_plural = _('Рецепты')

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        to=User,
        verbose_name=_('Пользователь'),
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        to=Recipe,
        verbose_name=_('Рецепт'),
        on_delete=models.CASCADE,
        related_name='additions',
    )

    class Meta:
        app_label = 'api'
        ordering = ('id', )
        verbose_name = _('Избранный рецепт')
        verbose_name_plural = _('Избранные рецепты')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='user_and_recipe_uniq_together',
            ),
        ]


class Purchase(models.Model):
    user = models.ForeignKey(
        to=User,
        verbose_name=_('Пользователь'),
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        to=Recipe,
        verbose_name=_('Рецепт'),
        on_delete=models.CASCADE,
        related_name='purchases',
    )

    class Meta:
        app_label = 'api'
        ordering = ('id', )
        verbose_name = _('Покупка')
        verbose_name_plural = _('Покупки')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='user_and_purchase_uniq_together',
            ),
        ]
