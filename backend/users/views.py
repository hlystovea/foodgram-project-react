from djoser.views import UserViewSet

from api.pagination import CustomPagination


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomPagination
