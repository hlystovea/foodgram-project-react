from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.db.models import Count, Exists, OuterRef
from django.utils.translation import gettext_lazy as _
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subscription
from api.pagination import CustomPagination
from .serializers import (SubscriptionReadSerializer,
                          SubscriptionWriteSerializer)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return self.queryset
        subscription = Subscription.objects.filter(
            author=OuterRef('pk'),
            user=user
        )
        return self.queryset.annotate(is_subscribed=Exists(subscription))

    @action(['get'], False, permission_classes=[IsAuthenticated])
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
            serializer = SubscriptionReadSerializer(
                page,
                context=context,
                many=True,
            )
            return self.get_paginated_response(serializer.data)

        serializer = SubscriptionReadSerializer(
            queryset,
            context=context,
            many=True,
        )
        return Response(serializer.data, status=HTTPStatus.OK)

    @action(['get', 'delete'], True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        if request.method == 'GET':
            context = {'request': request}
            data = {'author': id}
            serializer = SubscriptionWriteSerializer(
                data=data,
                context=context,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = SubscriptionReadSerializer(author, context=context)
            return Response(serializer.data, status=HTTPStatus.CREATED)
        if request.method == 'DELETE':
            obj = Subscription.objects.filter(user=request.user, author=author)
            if obj.exists():
                obj.delete()
                return Response(status=HTTPStatus.NO_CONTENT)
            message = {'errors': _('Подписка не найдена.')}
            return Response(message, status=HTTPStatus.BAD_REQUEST)
        return None
