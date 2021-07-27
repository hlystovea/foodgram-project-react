from django.contrib.auth import get_user_model
from django.http import FileResponse
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from . import serializers
from .filters import IngredientFilter, RecipeFilter
from .models import Favorite, Ingredient, Purchase, Quantity, Recipe, Tag
from .permissions import IsAdminOrAuthorOrReadOnly
from .utils import binder, get_pdf

User = get_user_model()


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    permission_classes = [AllowAny]
    filter_class = IngredientFilter
    pagination_class = None


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    permission_classes = [IsAdminOrAuthorOrReadOnly]
    filter_class = RecipeFilter

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return self.queryset
        return self.queryset.with_user(user)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.RecipeSerializer
        return serializers.RecipeWriteSerializer

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        user = self.request.user
        purchases = Quantity.objects.purchases(user)
        file = get_pdf(purchases)
        return FileResponse(file, as_attachment=True, filename='purchases.pdf')

    @action(
        methods=['get', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        return binder(request, pk, Favorite, serializers.FavoriteSerializer)

    @action(
        methods=['get', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):
        return binder(request, pk, Purchase, serializers.PurchaseSerializer)
