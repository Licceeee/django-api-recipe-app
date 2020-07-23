from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient

from recipe import serializers


class BaseAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                      mixins.CreateModelMixin):
    """Base class for user owned recipe/tag attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """return objs for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new obj"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseAttrViewSet):
    """Manage tags in the db"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseAttrViewSet):
    """Manage ingredients in the db"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
