from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.cache import cache
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_ratelimit.decorators import ratelimit
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from activity.utils import create_action, ActionType
from social_network.paginators import SmallPagination
from user.models import User
from user.serializers import UserSerializer, BlockUserSerializer


class CreateUserView(generics.CreateAPIView):

    serializer_class = UserSerializer
    queryset = User.objects.all()


@method_decorator(ratelimit(key='ip', rate='30/m', method='POST'), name='post')
class LoginView(TokenObtainPairView):
    pass


@method_decorator(cache_page(60 * 5), name='dispatch')
class UserSearchView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = SmallPagination

    def get_queryset(self):

        search_query = self.request.query_params.get('q')

        if search_query:

            vector = SearchVector('username', weight='A') + SearchVector('email', weight='B')
            query = SearchQuery(search_query)

            return (
                User.objects.annotate(rank=SearchRank(vector, query))
                .filter(Q(username__icontains=search_query) | Q(email__icontains=search_query))
                .order_by('-rank')
            )

        return User.objects.all().order_by('username')


class UserFriendsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        user_id = self.request.user.id
        cache_key = f'user_friends_{user_id}'
        friends = cache.get(cache_key)

        if not friends:
            friends = self.request.user.friends.all().order_by('username')
            cache.set(cache_key, friends, timeout=60 * 10)

        return friends


class BlockUserView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = BlockUserSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        return self.request.user.blocked_by.all().order_by('blocked__username')

    def perform_create(self, serializer):
        user_block = serializer.save()
        create_action(
            user=self.request.user,
            target_user=user_block.blocked,
            action_type=ActionType.USER_BLOCKED,
        )


class UnBlockUserView(generics.DestroyAPIView):

    lookup_field = 'blocked_id'
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.blocked_by.filter(blocked_id=self.kwargs['blocked_id'])

    def perform_destroy(self, instance):
        create_action(
            user=self.request.user,
            target_user=instance.blocked,
            action_type=ActionType.USER_UNBLOCKED,
        )
        instance.delete()
