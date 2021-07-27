from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

users_router = DefaultRouter()
users_router.register(r'users/subscriptions', views.SubscriptionViewSet, basename='subscriptions')
users_router.register(r'users', views.CustomUserViewSet, basename='users')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(users_router.urls)),
    path('', include('djoser.urls')),
]
