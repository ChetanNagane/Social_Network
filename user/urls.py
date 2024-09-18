from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.CreateUserView.as_view(), name='signup'),
    path('search/', views.UserSearchView.as_view(), name='search'),
    path('friends/', views.UserFriendsListView.as_view(), name='friends'),
    path('block/', views.BlockUserView.as_view(), name='block-user'),
    path('unblock/<int:blocked_id>', views.UnBlockUserView.as_view(), name='unblock-user'),
]
