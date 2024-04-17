from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserPresentationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    class Meta:
        model=User
        exclude = ('password', )


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
    )
    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {
            'username': {'required': False},
            "email": {'required': False},
        } 

    def validate(self, attrs):
        request = self.context['request']

        if request.data.get("username") is None and request.data.get("email") is None: 
            raise AttributeError('Auth by username or email')

        return super().validate(request.data)


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

        
        try:
            request.data['username']=user_obj.email
        except AttributeError:
            return AttributeError('afasdas')
        
        print(request.data)
        return super().validate(request.data)


class UserPasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, max_length=30, min_length=8)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance