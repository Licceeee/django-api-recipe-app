from django.contrib.auth import get_user_model  # noqa
from django.urls import reverse  # noqa
from django.test import TestCase  # noqa

from rest_framework import status  # noqa
from rest_framework.test import APIClient  # noqa

from core.models import Ingredient, Recipe  # noqa

from recipe.serializers import IngredientSerializer  # noqa


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientssApiTests(TestCase):
    """Test the publicly available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving ingredients"""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Test the authorized user ingredients API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """Test retrieving ingredients"""
        Ingredient.objects.create(user=self.user, name='Butter')
        Ingredient.objects.create(user=self.user, name='Honey')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that ingredients returned are for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@email.com',
            'testpass'
        )
        Ingredient.objects.create(user=user2, name='Fruity')
        ingredient = Ingredient.objects.create(user=self.user,
                                               name='Comfort Food')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """Test creating a new ingredient"""
        payload = {'name': 'Test Ingredient'}
        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user, name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_ingredient_invalid_name(self):
        """test creating new ingredient with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_ingredients_assigned_to_recipes(self):
        """Test filtering ingredients by those assigned to recipes"""
        ingredient1 = Ingredient.objects.create(user=self.user, name="Vegan")
        ingredient2 = Ingredient.objects.create(
            user=self.user, name="Vegetarian")
        recipe = Recipe.objects.create(
            user=self.user,
            title="Tikka Maala",
            time_minutes=17,
            price=8.00
        )
        recipe.ingredients.add(ingredient1)
        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

        serializer1 = IngredientSerializer(ingredient1)
        serializer2 = IngredientSerializer(ingredient2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_ingredients_assigned_unique(self):
        """Test filtering ingredients by assigned returns unique items"""
        ingredient = Ingredient.objects.create(user=self.user, name="Vegan")
        Ingredient.objects.create(user=self.user, name="Vegetarian")

        recipe1 = Recipe.objects.create(
            user=self.user,
            title="Chicken wings",
            time_minutes=15,
            price=8.00
        )
        recipe1.ingredients.add(ingredient)

        recipe2 = Recipe.objects.create(
            user=self.user,
            title="Pancakes",
            time_minutes=6,
            price=3.00
        )
        recipe2.ingredients.add(ingredient)
        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})
        self.assertEqual(len(res.data), 1)
        self.assertTrue(len(res.data), 1)
