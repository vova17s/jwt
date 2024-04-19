from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme

from authsystem.backend import JWTAuthentication


class SimpleJWTTokenUserScheme(SimpleJWTScheme):
    name = "CustomJWTAuth"
    target_class = JWTAuthentication