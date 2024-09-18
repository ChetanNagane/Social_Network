from django.urls import path

from friend_request import views

urlpatterns = [
    path('send/', views.SentFriendRequestView.as_view(), name='token_obtain_pair'),
    path('<int:sender_id>/', views.FriendRequestAccecptRejectView.as_view(), name='accept-reject-request'),
    path('pending/', views.FriendRequestListPendingView.as_view(), name='pending-request'),
]
