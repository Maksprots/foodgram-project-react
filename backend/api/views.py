from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (SAFE_METHODS, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from django.conf import settings

from recipes.models import (Cart, FavoriteRecipe, Ingredient, Recipe,
                            Subscribe, Tag)

from .filters import IngredientFilter, RecipesFilter
from .mixins import CreateDestroyViewSet
from .permissions import IsAuthorOrReadOnly
from .serializers import (CartSerializer, FavoriteRecipeSerializer,
                          IngredientSerializer, RecipeEditSerializer,
                          RecipeReadSerializer, SetPasswordSerializer,
                          SubscribeSerializer, TagSerializer,
                          UserCreateSerializer, UserListSerializer)
from users.User import User


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly)
    filterset_class = RecipesFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeEditSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'favorited': set(FavoriteRecipe.objects.filter(
                user_id=self.request.user
            ).values_list('favorite_recipe', flat=True)),
            'in_shopping_cart': set(Cart.objects.filter(
                user_id=self.request.user
            ).values_list('recipe_cart', flat=True))
        }


@action(
    detail=False,
    methods=('get',),
    url_path='download_shopping_cart',
    pagination_class=None)
def download_file(self, request):
    user = request.user
    if not user.cart.exists():
        return Response(
            settings.EMPTY_CART, status=status.HTTP_400_BAD_REQUEST)

    text = settings.SHOPPING_LIST + '\n\n'
    ingredient_name = 'recipe__recipe__ingredient__name'
    ingredient_unit = 'recipe__recipe__ingredient__measurement_unit'
    recipe_amount = 'recipe__recipe__amount'
    amount_sum = 'recipe__recipe__amount__sum'
    cart = user.cart.select_related('recipe').values(
        ingredient_name, ingredient_unit).annotate(Sum(recipe_amount)) \
        .order_by(ingredient_name)
    for _ in cart:
        text += (
            f'{_[ingredient_name]} ({_[ingredient_unit]})'
            f' — {_[amount_sum]}\n'
        )
    response = HttpResponse(text, content_type='text/plain')
    filename = 'shopping_list.txt'
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None
    filterset_class = IngredientFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'set_password':
            return SetPasswordSerializer
        if self.action == 'create':
            return UserCreateSerializer
        return UserListSerializer

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_serializer_context(self):

        return {'request': self.request,
                'format': self.format_kwarg,
                'view': self,
                'subscriptions': set(
                    Subscribe.objects.filter(
                        user_id=self.request.user
                    ).values_list('author_id', flat=True)
                )
                }

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        queryset = Subscribe.objects.filter(user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request}, )
        return self.get_paginated_response(serializer.data)


class SubscribeViewSet(CreateDestroyViewSet):
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        return self.request.user.follower.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['author_id'] = self.kwargs.get('user_id')
        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            author=get_object_or_404(
                User,
                id=self.kwargs.get('user_id')
            )
        )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'subscriptions': set(
                Subscribe.objects.filter(
                    user_id=self.request.user
                ).values_list('author_id', flat=True)
            )
        }

    @action(methods=('delete',), detail=True)
    def delete(self, request, user_id):
        get_object_or_404(User, id=user_id)
        if not Subscribe.objects.filter(
                user=request.user, author_id=user_id).exists():
            return Response({'errors': settings.ERROR_FOLLOW_AUTHOR},
                            status=status.HTTP_400_BAD_REQUEST)
        get_object_or_404(
            Subscribe,
            user=request.user,
            author_id=user_id
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteRecipeViewSet(CreateDestroyViewSet):
    serializer_class = FavoriteRecipeSerializer

    def get_queryset(self):
        user = self.request.user.id
        return FavoriteRecipe.objects.filter(user=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['recipe_id'] = self.kwargs.get('recipe_id')
        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            favorite_recipe=get_object_or_404(
                Recipe,
                id=self.kwargs.get('recipe_id')
            )
        )

    @action(methods=('delete',), detail=True)
    def delete(self, request, recipe_id):
        u = request.user
        if not u.favorite.select_related(
                'favorite_recipe').filter(favorite_recipe_id=recipe_id) \
                .exists():
            return Response({'errors': settings.ERROR_FAVORITE_RECIPE},
                            status=status.HTTP_400_BAD_REQUEST)
        get_object_or_404(
            FavoriteRecipe,
            user=request.user,
            favorite_recipe_id=recipe_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartViewSet(CreateDestroyViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user.id
        return Cart.objects.filter(user=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['recipe_id'] = self.kwargs.get('recipe_id')
        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            recipe=get_object_or_404(
                Recipe,
                id=self.kwargs.get('recipe_id')
            )
        )

    @action(methods=('delete',), detail=True)
    def delete(self, request, recipe_id):
        u = request.user
        if not u.shopping_cart.select_related(
                'recipe').filter(recipe_id=recipe_id).exists():
            return Response({'errors': settings.ERROR_RECIPE_DOESNT_CART},
                            status=status.HTTP_400_BAD_REQUEST)
        get_object_or_404(
            Cart,
            user=request.user,
            recipe=recipe_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
