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
        on_delete=models.CASCADE,
        related_name='quantities'
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name=_('Количество'),
        validators=[
            validators.MaxValueValidator(
                10000,
                message='Слишком много, проверьте единицы измерения',
            ),
        ]
    )

    class Meta:
        app_label = 'api'
        ordering = ('ingredient', )
        verbose_name = _('Кол-во ингредиента')
        verbose_name_plural = _('Кол-ва ингредиентов')

    def __str__(self):
        name = self.ingredient.name
        quantity = self.quantity
        measurement_unit = self.ingredient.measurement_unit
        return f'{name}: {quantity} {measurement_unit}'


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
    ingredients = models.ManyToManyField(
        to=Quantity,
        verbose_name=_('Ингредиенты'),
        related_name='recipes',
    )
    text = models.TextField(
        verbose_name=_('Рецепт'),
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name=_('Время приготовления, мин'),
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
    tags = models.ManyToManyField(
        to=Tag,
        verbose_name=_('Теги'),
        related_name='recipes',
    )

    class Meta:
        app_label = 'api'
        ordering = ('-id', )
        verbose_name = _('Рецепт')
        verbose_name_plural = _('Рецепты')

    def __str__(self):
        return self.name
