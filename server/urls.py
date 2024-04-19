from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("openapi.urls")),
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('authsystem.urls')),
]
