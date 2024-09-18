from django.urls import path, include

urlpatterns = [
    path('v1/', include('social_network.api.v1')),
    path('api-auth/', include('rest_framework.urls')),
]
