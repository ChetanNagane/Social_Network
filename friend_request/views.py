from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_ratelimit.decorators import ratelimit
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from activity.utils import create_action, ActionType
from friend_request.models import FriendRequest
from friend_request.serializers import (
    FriendRequestSentSerializer,
    FriendRequestAccecptRejectSerializer,
    FriendRequestListSerializer,
)
from social_network.paginators import SmallPagination


@method_decorator(ratelimit(key='ip', rate='3/m', method='POST'), name='post')
class SentFriendRequestView(generics.CreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = FriendRequestSentSerializer
    queryset = FriendRequest.objects.all()

    def perform_create(self, serializer):
        friend_request = serializer.save()
        create_action(
            user=self.request.user,
            target_user=friend_request.receiver,
            action_type=ActionType.REQUEST_SENT,
        )


class FriendRequestAccecptRejectView(generics.UpdateAPIView):

    lookup_field = 'sender_id'
    permission_classes = (IsAuthenticated,)
    serializer_class = FriendRequestAccecptRejectSerializer
    queryset = FriendRequest.objects.all()

    def get_queryset(self):
        return FriendRequest.objects.filter(
            receiver=self.request.user, status='pending', sender_id=self.kwargs['sender_id']
        )

    def perform_update(self, serializer):
        friend_request = serializer.save()
        if friend_request.status == 'accepted':
            create_action(
                user=self.request.user,
                target_user=friend_request.sender,
                action_type=ActionType.REQUEST_ACCECPTED,
            )
        elif friend_request.status == 'rejected':
            create_action(
                user=self.request.user,
                target_user=friend_request.sender,
                action_type=ActionType.REQUEST_REJECTED,
            )


@method_decorator(cache_page(60 * 2), name='dispatch')
class FriendRequestListPendingView(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = FriendRequestListSerializer
    pagination_class = SmallPagination
    ordering_fields = ('timestamp',)
    filter_backends = (OrderingFilter,)

    def get_queryset(self):
        return FriendRequest.objects.filter(receiver=self.request.user, status='pending')
