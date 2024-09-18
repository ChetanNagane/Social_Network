from django.urls import path, include

urlpatterns = [
    path('user/', include('user.urls')),
    path('friend-request/', include('friend_request.urls')),
    path('activity/', include('activity.urls')),
]
