from django.db import models
from django.utils.translation import gettext_lazy as _


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Ингредиенты',
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=200,
    )

    class Meta:
        app_label = 'api'
        ordering = ('name',)
        verbose_name = _('Ингредиент')
        verbose_name_plural = _('Ингредиенты')

    def __str__(self):
        return self.name
