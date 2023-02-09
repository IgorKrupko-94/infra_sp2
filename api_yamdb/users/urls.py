from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import APIGetToken, APISignup, UserViewSet

v1_router = DefaultRouter()
v1_router.register(
    'users',
    UserViewSet,
    basename='users'
)

urlauth = [
    path('auth/signup/', APISignup.as_view(), name='signup'),
    path('auth/token/', APIGetToken.as_view(), name='get_token')
]

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include(urlauth))
]
