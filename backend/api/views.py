from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Exists, F, OuterRef, Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, pagination, permissions, status, views, viewsets
from rest_framework.response import Response

from . import models, serializers

User = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    pagination_class = None


class QuantityViewSet(viewsets.ModelViewSet):
    queryset = models.Quantity.objects.all()
    serializer_class = serializers.QuantitySerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.RecipeSerializer
        return serializers.RecipeWriteSerializer


class SubscriptionListView(mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    queryset = models.Subscription.objects.all()
    serializer_class = serializers.SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        is_subscribed = models.Subscription.objects.filter(
            author=OuterRef('pk'), user=user)
        return User.objects.filter(subscribers__user=user) \
                           .annotate(recipes_count=Count('recipes')) \
                           .annotate(is_subscribed=Exists(is_subscribed))


class SubscriptionWriteView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        user = request.user
        author = get_object_or_404(User, pk=pk)
        subscription, created = models.Subscription.objects.get_or_create(user=user, author=author)
        if created:
            return Response(status=status.HTTP_201_CREATED)
        message = {'errors': _(f'Вы уже подписаны на {author}.')}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        user = request.user
        author = get_object_or_404(User, pk=pk)
        subscription = models.Subscription.objects.filter(user=user, author=author)
        if subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        message = {'errors': _('Подписка не найдена.')}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
