from rest_framework import serializers

from core.models import Tag, Ingredient


class TagSerializer(serializers.HyperlinkedModelSerializer):
    """Serializers for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    """Serializers for ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name',)
        read_only_fields = ('id',)
