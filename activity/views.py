from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from activity.filters import ActionFilter
from activity.models import Action
from activity.serializers import ActionSerializer
from social_network.paginators import SmallPagination


class ActionListAPIView(generics.ListAPIView):
    name = 'Action List API'

    filterset_class = ActionFilter
    serializer_class = ActionSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = SmallPagination

    def get_queryset(self) -> QuerySet:
        return Action.objects.all().select_related('user').only(*ActionSerializer.only_fields).order_by('-timestamp')
