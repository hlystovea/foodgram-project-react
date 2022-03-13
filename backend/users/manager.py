from django.contrib.auth.models import UserManager
from django.db.models import Count, Exists, OuterRef

from . import models


class CustomUserManager(UserManager):
    def with_user(self, user):
        subscription = models.Subscription.objects.filter(
            author=OuterRef('pk'),
            user=user,
        )
        return self.annotate(is_subscribed=Exists(subscription))

    def custom_subscriptions(self, user):
        subscription = models.Subscription.objects.filter(
            author=OuterRef('pk'),
            user=user,
        )
        return self.filter(subscribers__user=user) \
                   .annotate(recipes_count=Count('recipes')) \
                   .annotate(is_subscribed=Exists(subscription))
