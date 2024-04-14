from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings
from .models import User
from .backend import JWTAuthentication
from jwt_test.settings import SIMPLE_JWT


class UserPresentationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    class Meta:
        model=User
        exclude = ('password', )


class RegisterUserSerializer(serializers.ModelSerializer):
    is_active = serializers.ReadOnlyField()
    is_staff = serializers.ReadOnlyField()
    is_superuser = serializers.ReadOnlyField()
    password = serializers.CharField(
        max_length=128,
        min_length=8,
    )
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user



class CustomObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'
    
    def validate(self, attrs):
        user_obj = User.objects.filter(email=attrs.get(self.username_field)).first()
        if user_obj is None:
            user_obj = User.objects.filter(username=attrs.get(self.username_field)).first()
        
        request = self.context['request']
        request.data._mutable = True
        
        try:
            request.data['username']=user_obj.email
        except:
            return AttributeError('afasdas')
        
        request.data._mutable = False
        print(request.data)
        return super().validate(request.data)
