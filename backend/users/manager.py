from django.db.models import Exists, F, QuerySet, OuterRef, Sum

from . import models

class CustomUserQuerySet(QuerySet):
    def with_user(self, user):
        subscription = models.Subscription.objects.filter(
            author=OuterRef('pk'),
            user=user,
        )
        return self.annotate(is_subscribed=Exists(subscription))
