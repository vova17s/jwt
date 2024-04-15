import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from .models import User


class JWTAuthentication(BaseAuthentication):
    
    def authenticate(self, request, *args, **kwargs):
        headers = get_authorization_header(request)
        username = request.data.get('username')
        email = request.data.get('email')
        
        if headers:
            return self._auth_by_jwt(headers)
        
        if email:
            password = request.data.get('password')
            return self._auth_by_email(email=email, password=password)
        
        if username:
            password = request.data.get('password')
            return self._auth_by_username(username=username, password=password)
        return None, False    
    
    
    def _auth_by_jwt(self, headers):
        auth_data = headers.decode('utf-8')
        auth_token = auth_data.split()
        
        if len(auth_token) != 2:
            return None, False
        
        payload = auth_token[1]
        header = jwt.get_unverified_header(payload)

        try:
            decode_payload = jwt.decode(payload, settings.SECRET_KEY, header['alg'])
        except jwt.ExpiredSignatureError:
            raise TypeError('Invalid token signature ', status.HTTP_401_UNAUTHORIZED)
        
        try:
            user = User.objects.get(pk=decode_payload["user_id"])
            return user, True
        except:
            return None, False
        
        
    def _auth_by_email(self, email, password):
        try:
            user = User.objects.get(email=email)
        except:
            return None, False

        if user.check_password(password):
            return user, True


    def _auth_by_username(self, username, password):
        try:
            user = User.objects.get(username=username)
        except:
            return None, False

        if user.check_password(password):
            return user, True
        return None, False
