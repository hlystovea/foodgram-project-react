from django.contrib.auth import get_user_model
from django.db.models import Exists, F, OuterRef, Sum
from django.http import FileResponse
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from . import serializers
from .filters import IngredientFilter, RecipeFilter
from .models import Ingredient, Favorite, Quantity, Tag, Recipe, Purchase
from .pagination import CustomPagination
from .utils import binder, get_pdf

User = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    permission_classes = [permissions.AllowAny]
    filter_class = IngredientFilter
    pagination_class = None


class QuantityViewSet(viewsets.ModelViewSet):
    queryset = Quantity.objects.all()
    serializer_class = serializers.QuantitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_class = RecipeFilter
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return self.queryset
        favorites = Favorite.objects.filter(recipe=OuterRef('pk'), user=user)
        purchases = Purchase.objects.filter(recipe=OuterRef('pk'), user=user)
        return self.queryset.annotate(is_favorited=Exists(favorites)) \
                            .annotate(is_in_shopping_cart=Exists(purchases))

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.RecipeSerializer
        return serializers.RecipeWriteSerializer

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        ingredients = Quantity.objects.filter(
            recipe__purchases__user=request.user
        )
        purchases = ingredients.values(
            name=F('ingredient__name'),
            unit=F('ingredient__measurement_unit'),
        ).annotate(
            total=Sum('amount'),
        )
        file = get_pdf(purchases)
        return FileResponse(file, as_attachment=True, filename='purchases.pdf')

    @action(
        methods=['get', 'delete'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        return binder(request, recipe, Favorite)

    @action(
        methods=['get', 'delete'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        return binder(request, recipe, Purchase)
