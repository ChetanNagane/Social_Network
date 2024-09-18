from django.urls import path

from activity import views

app_name = 'activity'

urlpatterns = [
    path('', views.ActionListAPIView.as_view(), name='action-list'),
]
