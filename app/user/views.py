from rest_framework import generics
from rest_framework.authtoken import views
from rest_framework.settings import api_settings
from user.serializers import (UserSerializer, AuthTokenSerializer)


class CreateUserView(generics.CreateAPIView):
    """Create a new user"""
    serializer_class = UserSerializer


class CreateTokenView(views.ObtainAuthToken):
    """Create a new authtoken for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
