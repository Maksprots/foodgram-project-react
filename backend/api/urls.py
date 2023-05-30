from django.urls import include, path
from rest_framework import routers
from django.views.generic import TemplateView

from .views import (CustomUserViewSet, FavoriteRecipeViewSet,
                    IngredientViewSet, RecipeViewSet, CartViewSet,
                    SubscribeViewSet, TagViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register(r'users/(?P<user_id>\d+)/subscribe', SubscribeViewSet,
                basename='subscribe')
router.register(r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteRecipeViewSet,
                basename='favorite')
router.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart', CartViewSet,
                basename='cart')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
