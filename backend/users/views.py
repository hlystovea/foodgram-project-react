from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.db.models import Count, Exists, OuterRef
from django.utils.translation import gettext_lazy as _
from djoser.views import UserViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.models import Subscription
from api.pagination import CustomPagination
from .serializers import SubscriptionSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomPagination

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        pagination_class=CustomPagination,
    )
    def subscriptions(self, request):
        user = self.request.user
        subscribtion = Subscription.objects.filter(
            author=OuterRef('pk'),
            user=user,
        )
        queryset = User.objects.filter(subscribers__user=user) \
                               .annotate(recipes_count=Count('recipes')) \
                               .annotate(is_subscribed=Exists(subscribtion))
        context = {'request': request}
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscriptionSerializer(page, context=context, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = SubscriptionSerializer(queryset, context=context, many=True)
        return Response(serializer.data, status=HTTPStatus.OK)

    @action(
        methods=['get', 'delete'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'GET':
            obj, created = Subscription.objects.get_or_create(
                user=user,
                author=author,
            )
            if created:
                context = {'request': request}
                serializer = SubscriptionSerializer(author, context=context)
                return Response(serializer.data, status=HTTPStatus.CREATED)
        message = {'errors': _(f'Вы уже подписаны на {author}.')}
        if request.method == 'DELETE':
            obj = Subscription.objects.filter(user=user, author=author)
            if obj.exists():
                obj.delete()
                return Response(status=HTTPStatus.NO_CONTENT)
            message = {'errors': _('Подписка не найдена.')}
        return Response(message, status=HTTPStatus.BAD_REQUEST)
