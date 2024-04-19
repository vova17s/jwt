from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from services import DefaultPagination

from .backend import JWTAuthentication
from .models import User
from .serializers import (
    CustomObtainPairSerializer,
    RegisterUserSerializer,
    UserPasswordChangeSerializer,
    UserPresentationSerializer,
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserPresentationSerializer
    pagination_class = DefaultPagination
    permission_classes = (IsAuthenticated, )


class SupportAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPresentationSerializer

    def get(self, request) -> Response:
        if request.user:
            return Response(self.serializer_class(request.user).data, 200)

        return Response({"detail": "No user"}, 401)


class UserRegistrationView(TokenObtainPairView):
    serializer_class = RegisterUserSerializer
    support_serializer = CustomObtainPairSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        data = self.serializer_class(data=request.data)
        if data.is_valid():
            data.save()
            serializer = self.support_serializer(context= super(UserRegistrationView, self).get_serializer_context(), data={'username': request.data['username'], 'password': request.data['password']})
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(data.errors, status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(GenericAPIView):
    serializer_class = UserPasswordChangeSerializer
    permission_classes = (IsAuthenticated, )
    auth_backend = JWTAuthentication()

    def post(self, request, *args, **kwargs) -> Response:
        user = request.user

        if not user:
            return Response({'detail': 'Denied change password'}, status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data, instance=user)

        if not serializer.is_valid(raise_exception=True):
            return Response({'detail': 'Success change password'}, status.HTTP_202_ACCEPTED)

        serializer.save()

        return Response({'detail': 'Not a valid token'}, status.HTTP_400_BAD_REQUEST)
