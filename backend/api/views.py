from django.contrib.auth import get_user_model
from django.db.models import Count, Exists, OuterRef
from django.http import FileResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import mixins, pagination, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import Ingredient, Favorite, Quantity, Tag, Recipe, Subscription, Purchase
from .filters import IngredientFilter, RecipeFilter
from .utils import get_shopping_list

User = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    filter_class = IngredientFilter
    pagination_class = None


class QuantityViewSet(viewsets.ModelViewSet):
    queryset = Quantity.objects.all()
    serializer_class = serializers.QuantitySerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_class = RecipeFilter
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        favorites = Favorite.objects.filter(recipe=OuterRef('pk'), user=user)
        purchases = Purchase.objects.filter(recipe=OuterRef('pk'), user=user)
        return Recipe.objects.annotate(is_favorited=Exists(favorites)) \
                             .annotate(is_in_shopping_cart=Exists(purchases))

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.RecipeSerializer
        return serializers.RecipeWriteSerializer

    @action(methods=['get'], detail=False)
    def download_shopping_cart(self, request):
        recipes = self.get_queryset().filter(is_in_shopping_cart=True)
        ingredients = Quantity.objects.filter(recipe__in=recipes)
        file = get_shopping_list(ingredients)
        return FileResponse(file, as_attachment=True, filename='purchases.pdf')


class FavoriteWriteView(APIView):
    lookup_field = 'id'
    lookup_value_regex = '[0-9]{32}'
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        obj, created = Favorite.objects.get_or_create(user=user, recipe=recipe)
        if created:
            serializer = serializers.RecipeLiteSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        message = {'errors': _(f'Рецепт {recipe} уже есть в избранное.')}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite = Favorite.objects.filter(user=user, recipe=recipe)
        if favorite.exists():
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        message = {'errors': _('Этого рецепта нет в вашем списке избранного.')}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionListView(mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    queryset = Subscription.objects.all()
    serializer_class = serializers.SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        subscribtions = Subscription.objects.filter(
                                     author=OuterRef('pk'), user=user)
        return User.objects.filter(subscribers__user=user) \
                           .annotate(recipes_count=Count('recipes')) \
                           .annotate(is_subscribed=Exists(subscribtions))


class SubscriptionWriteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        user = request.user
        author = get_object_or_404(User, pk=pk)
        obj, created = Subscription.objects.get_or_create(
                                            user=user, author=author)
        if created:
            return Response(status=status.HTTP_201_CREATED)
        message = {'errors': _(f'Вы уже подписаны на {author}.')}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        user = request.user
        author = get_object_or_404(User, pk=pk)
        subscription = Subscription.objects.filter(user=user, author=author)
        if subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        message = {'errors': _('Подписка не найдена.')}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class PurchaseWriteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        obj, created = Purchase.objects.get_or_create(user=user, recipe=recipe)
        if created:
            serializer = serializers.RecipeLiteSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        message = {'errors': _(f'Рецепт {recipe} уже есть в вашем списке.')}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        purchase = Purchase.objects.filter(user=user, recipe=recipe)
        if purchase.exists():
            purchase.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        message = {'errors': _('Этого рецепта нет в вашем списке.')}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
