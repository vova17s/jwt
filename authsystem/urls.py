from django.urls import path
from rest_framework.routers import SimpleRouter

from .auth_views import (
    ChangePasswordView,
    LoginAPIView,
    RefreshAPIView,
    SupportAPIView,
    UserRegistrationView,
    VerifyAPIView,
)
from .user_views import UserViewSet

router = SimpleRouter()
router.register('user', UserViewSet)


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register_user'),
    path('me/', SupportAPIView.as_view(), name='support'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('refresh/', RefreshAPIView.as_view(), name='token_refresh'),
    path('verify/', VerifyAPIView.as_view(), name='token_verify'),
    path('login/', LoginAPIView.as_view(), name='token_obtain_pair'),
]

urlpatterns += router.urls