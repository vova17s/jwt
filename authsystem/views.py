from tokenize import TokenError

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
        auth_class = JWTAuthentication()
        user, success = auth_class.authenticate(request)
        if success:
            return Response(self.serializer_class(user).data, 200)
        return Response({"detail": "Invalid data"}, 404)


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
    def get_user(self):
        auth_class = JWTAuthentication()
        return auth_class.authenticate(self.request)[0]
    
    def put(self, request, *args, **kwargs) -> Response:
        user = self.get_user()
        if user:
            serializer = self.serializer_class(data=request.data, instance=user)
        
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'detail': 'Success change password'}, status.HTTP_202_ACCEPTED)
            
            return Response({'detail': 'Denied change password'}, status.HTTP_400_BAD_REQUEST)
                
        raise TokenError({'detail': "Not a valid token"}, status.HTTP_400_BAD_REQUEST)