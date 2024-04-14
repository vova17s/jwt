from django.shortcuts import render
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .backend import JWTAuthentication
from .models import User
from .serializers import RegisterUserSerializer, UserPresentationSerializer, CustomObtainPairSerializer


class UserPagination(PageNumberPagination):
    page_size = 50
    max_page_size = 500
    page_size_query_param = 'page_size'


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserPresentationSerializer
    pagination_class = UserPagination
    permission_classes = (IsAuthenticated, )


class SupportAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
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
