from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from common import routers

custom_router = routers.CustomRouter()
custom_router.register(
    r'recipes/(?P<recipe_id>\d+)/favorite',
    views.FavoriteViewSet,
    basename='favorites',
)
custom_router.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    views.PurchaseViewSet,
    basename='shopping_cart',
)


v1_router = DefaultRouter()
v1_router.register(r'tags', views.TagViewSet, basename='tags')
v1_router.register(r'recipes', views.RecipeViewSet, basename='recipes')
v1_router.register(
    r'ingredients',
    views.IngredientViewSet,
    basename='ingredients',
)


urlpatterns = [
    path('', include(custom_router.urls)),
    path('', include(v1_router.urls)),
]
