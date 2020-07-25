from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe


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


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    """Serializers for Recipe objects"""
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Ingredient.objects.all(),)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(),)

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingredients', 'tags', 'price',
                  'time_minutes', 'link')
        read_only_fields = ('id',)
