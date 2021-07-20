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
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(v1_router.urls)),
]
