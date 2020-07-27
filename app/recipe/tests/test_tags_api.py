from django.contrib.auth import get_user_model  # noqa
from django.urls import reverse  # noqa
from django.test import TestCase  # noqa

from rest_framework import status  # noqa
from rest_framework.test import APIClient  # noqa

from core.models import Tag, Recipe  # noqa

from recipe.serializers import TagSerializer  # noqa


TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@emal.com',
            'password'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@email.com',
            'testpass'
        )
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {'name': 'Test Tag'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user, name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_tag_invalid_name(self):
        """test creating new tag with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_tags_assigned_to_recipes(self):
        """Test filtering tags by those assigned to recipes"""
        tag1 = Tag.objects.create(user=self.user, name="Vegan")
        tag2 = Tag.objects.create(user=self.user, name="Vegetarian")
        recipe = Recipe.objects.create(
            user=self.user,
            title="Tikka Maala",
            time_minutes=17,
            price=8.00
        )
        recipe.tags.add(tag1)
        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_tags_assigned_unique(self):
        """Test filtering tags by assigned returns unique items"""
        tag = Tag.objects.create(user=self.user, name="Vegan")
        Tag.objects.create(user=self.user, name="Vegetarian")

        recipe1 = Recipe.objects.create(
            user=self.user,
            title="Chicken wings",
            time_minutes=15,
            price=8.00
        )
        recipe1.tags.add(tag)

        recipe2 = Recipe.objects.create(
            user=self.user,
            title="Pancakes",
            time_minutes=6,
            price=3.00
        )
        recipe2.tags.add(tag)
        res = self.client.get(TAGS_URL, {'assigned_only': 1})
        self.assertEqual(len(res.data), 1)
        self.assertTrue(len(res.data), 1)
