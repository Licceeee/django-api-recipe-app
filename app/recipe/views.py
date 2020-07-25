from rest_framework import viewsets, mixins  # noqa
from rest_framework.authentication import TokenAuthentication  # noqa
from rest_framework.permissions import IsAuthenticated  # noqa

from core.models import Tag, Ingredient, Recipe  # noqa

from recipe import serializers  # noqa


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


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the db"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """return recipe for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        """Create a new obj"""
        serializer.save(user=self.request.user)
