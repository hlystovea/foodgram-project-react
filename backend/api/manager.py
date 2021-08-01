from django.db.models import Exists, F, QuerySet, OuterRef, Sum


class RecipeQuerySet(QuerySet):
    def with_user(self, user):
        from api.models import Favorite, Purchase

        favorites = Favorite.objects.filter(
            recipe=OuterRef('pk'),
            user=user,
        )
        purchases = Purchase.objects.filter(
            recipe=OuterRef('pk'),
            user=user,
        )
        return self.annotate(is_favorited=Exists(favorites)) \
                   .annotate(is_in_shopping_cart=Exists(purchases))


class QuantityQuerySet(QuerySet):
    def purchases(self, user):
        return self.filter(
            recipe__purchases__user=user
        ).values(
            name=F('ingredient__name'),
            unit=F('ingredient__measurement_unit'),
        ).annotate(
            total=Sum('amount'),
        )
