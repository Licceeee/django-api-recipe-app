from django.urls import path, include  # noqa
from rest_framework.routers import DefaultRouter  # noqa

from recipe import views  # noqa

router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('recipes', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
