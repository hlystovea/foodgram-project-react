from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views


v1_router = DefaultRouter()
v1_router.register(r'ingredients', views.IngredientViewSet, basename='ingredients')
v1_router.register(r'quantities', views.QuantityViewSet, basename='quantities')
v1_router.register(r'tags', views.TagViewSet, basename='tags')
v1_router.register(r'recipes', views.RecipeViewSet, basename='recipes')


urlpatterns = [
    path(
        'auth/token/',
        TokenObtainPairView.as_view(), name='token_obtain_pair'
    ),
    path(
        'auth/token/refresh/',
        TokenRefreshView.as_view(), name='token_refresh'
    ),
    path('', include('djoser.urls')),
    path('', include(v1_router.urls)),
]
