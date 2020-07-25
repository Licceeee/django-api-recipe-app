from django.contrib.auth import get_user_model  # noqa
from django.urls import reverse  # noqa
from django.test import TestCase  # noqa

from rest_framework import status  # noqa
from rest_framework.test import APIClient  # noqa

from core.models import Recipe, Tag, Ingredient  # noqa

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer  # noqa


RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """return recipe detail url"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_tag(user, name='Vegan'):
    """create & return sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='Chia'):
    """create & return sample tag"""
    return Ingredient.objects.create(user=user, name=name)


def sample_recipe(user, **params):
    """create and return a sample recipe"""
    defaults = {
        'title': 'Recipe Title',
        'time_minutes': 10,
        'price': 5
    }
    defaults.update(params)  # comes with dict, updates defaults

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipessApiTests(TestCase):
    """Test the publicly available recipes API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving recipes"""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipesApiTests(TestCase):
    """Test the authorized user recipes API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test that recipes returned are for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@email.com',
            'testpass'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        """test viewing a recipe detail"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recipe(self):
        """test creating recipe"""
        payload = {
            'title': 'Strawberry cake',
            'time_minutes': 35,
            'price': 5.00,
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):
        """test creating recipe with tags"""
        tag1 = sample_tag(user=self.user)
        tag2 = sample_tag(user=self.user, name='Dessert')
        payload = {
            'title': 'Strawberry cake',
            'time_minutes': 40,
            'price': 5.00,
            'tags': [tag1.id, tag2.id],
        }

        res = self.client.post(RECIPES_URL, payload)

        # create recipe
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # retrieve created recipe
        recipe = Recipe.objects.get(id=res.data['id'])
        # retrieve created tags
        tags = recipe.tags.all()
        # check that 3 created tags == 2 (tag1, tag2)
        self.assertEqual(tags.count(), 2)
        # check if tags created in sample tags r the same as in the queryset
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_recipe_with_ingredients(self):
        """test creating recipe with ingredients"""
        ingredient1 = sample_ingredient(user=self.user, name='Strawberry')
        ingredient2 = sample_ingredient(user=self.user, name='Butter')
        ingredient3 = sample_ingredient(user=self.user, name='Milk')
        payload = {
            'title': 'Strawberry cake',
            'time_minutes': 40,
            'price': 5.00,
            'ingredients': [ingredient1.id, ingredient2.id, ingredient3.id],
        }

        res = self.client.post(RECIPES_URL, payload)

        # create recipe
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # retrieve created recipe
        recipe = Recipe.objects.get(id=res.data['id'])
        # retrieve created tags
        ingredients = recipe.ingredients.all()
        # check that 3 created tags == 2 (tag1, tag2)
        self.assertEqual(ingredients.count(), 3)
        # check if tags created in sample tags r the same as in the queryset
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)
        self.assertIn(ingredient3, ingredients)
