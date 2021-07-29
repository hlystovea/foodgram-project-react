from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _

from . import models

User = get_user_model()


class MixinAdmin(admin.ModelAdmin):
    empty_value_display = _('-пусто-')


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name',
                    'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups'),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()
        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
                'user_permissions',
            }
        if (
            not is_superuser
            and obj is not None
            and (obj.is_superuser or obj == request.user)
        ):
            disabled_fields |= {
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }
        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
        return form


@admin.register(models.Subscription)
class SubscriptionAdmin(MixinAdmin):
    list_display = ('id', 'get_user', 'get_author')
    search_fields = ('user', 'author')
    autocomplete_fields = ('user', 'author')

    @admin.display(description=_('Пользователь'))
    def get_user(self, obj):
        user = obj.user
        url = (
            reverse('admin:users_customuser_changelist')
            + '?'
            + urlencode({'id': f'{user.id}'})
        )
        return format_html('<a href="{}">{}</a>', url, user)

    @admin.display(description=_('Автор'))
    def get_author(self, obj):
        author = obj.author
        url = (
            reverse('admin:users_customuser_changelist')
            + '?'
            + urlencode({'id': f'{author.id}'})
        )
        return format_html('<a href="{}">{}</a>', url, author)
