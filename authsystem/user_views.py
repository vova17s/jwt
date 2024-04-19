from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from services import DefaultPagination

from .models import User
from .serializers import (
    UserPresentationSerializer,
)


@extend_schema(tags=['User'])
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserPresentationSerializer
    pagination_class = DefaultPagination
    permission_classes = (IsAuthenticated, )

