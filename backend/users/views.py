from http import HTTPStatus

from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subscription
from .serializers import (SubscriptionReadSerializer,
                          SubscriptionWriteSerializer)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return self.queryset
        return self.queryset.with_user(user)


class SubscriptionViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SubscriptionReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.custom_subscriptions(self.request.user)


class SubscribeViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionWriteSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        author = get_object_or_404(User, pk=self.kwargs['author_id'])
        return self.request.user.subscriptions.filter(author=author)

    def create(self, request, *args, **kwargs):
        author = get_object_or_404(User, pk=self.kwargs['author_id'])
        context = {'request': request}
        data = {'author': self.kwargs['author_id']}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = SubscriptionReadSerializer(author, context=context)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=HTTPStatus.CREATED,
            headers=headers,
        )
