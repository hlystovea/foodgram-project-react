from django.core import validators
from django.db import models


class ColorField(models.CharField):
    """Поле для хранения HTML-кода цвета."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 7)
        super().__init__(*args, **kwargs)
        self.validators.append(validators.RegexValidator(r'#[A-Za-f\d]{6}'))
