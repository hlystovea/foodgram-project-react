from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager


class CustomUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Обязательное. 150 знаков или менее. \
             Только буквы, цифры и символы @/./+/-/_.'
        ),
        validators=[username_validator],
        error_messages={
            'unique': _('Пользователь с таким username уже существует.'),
        },
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _('Пользователь с таким email уже существует.'),
        },
    )
    objects = CustomUserManager()


class Subscription(models.Model):
    user = models.ForeignKey(
        to=CustomUser,
        verbose_name=_('Подписчик'),
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    author = models.ForeignKey(
        to=CustomUser,
        verbose_name=_('Автор'),
        on_delete=models.CASCADE,
        related_name='subscribers',
    )

    class Meta:
        app_label = 'users'
        ordering = ('id', )
        verbose_name = _('Подписка')
        verbose_name_plural = _('Подписки')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='sub_user_and_author_uniq_together',
            ),
        ]

    def __str__(self):
        return f'Подписка: {self.user.username} на {self.author.username}'

    def clean(self):
        errors = {}
        if self.user == self.author:
            errors['author'] = ValidationError(
                _('Пользователь не может быть подписан на самого себя.')
            )
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
