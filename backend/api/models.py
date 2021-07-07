from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import fields

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200,
    )

    class Meta:
        app_label = 'api'
        ordering = ('name', )
        verbose_name = _('Ингредиент')
        verbose_name_plural = _('Ингредиенты')

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        to=Ingredient,
        through='QuantityIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name=_('Ингредиенты'),
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        to='Tag',
        verbose_name=_('Теги'),
        related_name='recipes',
    )
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
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            validators.MinValueValidator(
                1,
                message='Время не может быть меньше 1 минуты',
            ),
            validators.MaxValueValidator(
                1000,
                message='Слишком долго, укажите время в минутах',
            ),
        ]
    )

    class Meta:
        app_label = 'api'
        ordering = ('-id', )
        verbose_name = _('Рецепт')
        verbose_name_plural = _('Рецепты')

    def __str__(self):
        return self.name


class QuantityIngredient(models.Model):
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        to=Ingredient,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveSmallIntegerField(
        validators=[
            validators.MaxValueValidator(
                10000,
                message='Слишком много, проверьте единицы измерения',
            ),
        ]
    )


class Tag(models.Model):
    name = models.CharField(
        verbose_name=_('Наименование'),
        max_length=200,
        unique=True,
    )
    color = fields.ColorField(
        verbose_name=_('Цвет'),
        default='#FF0000'
    )
    slug = models.SlugField(
        verbose_name=_('Слаг'),
        max_length=200,
        unique=True,
    )

    class Meta:
        app_label = 'api'
        ordering = ('name', )
        verbose_name = _('Тег')
        verbose_name_plural = _('Теги')

    def __str__(self):
        return self.name
