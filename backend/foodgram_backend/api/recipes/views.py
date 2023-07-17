from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.pagination import CustomPageNumberPagination
from api.permissons import IsAuthorOrReadOnlyPermission
from api.recipes.serializers import (
    RecipeSerializer, RecipeSerializerLite)
from recipes.models import Favorite, Recipe, ShoppingCart


class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = CustomPageNumberPagination

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe__id=pk).exists():
                return Response(
                    data={'error': 'This recipe already in favorite!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Favorite.objects.create(user=user, recipe=recipe)
            serializer = RecipeSerializerLite(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # DELETE
        favorite = Favorite.objects.filter(user=user, recipe=recipe)
        if not favorite.exists():
            return Response(
                data={'error': 'This recipe not in your favorites!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=user, recipe__id=pk).exists():
                return Response(
                    data={'error': 'This recipe already in shopping cart!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = RecipeSerializerLite(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # DELETE
        shopping_cart = ShoppingCart.objects.filter(user=user, recipe=recipe)
        if not shopping_cart.exists():
            return Response(
                data={'error': 'This recipe not in your shopping cart!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        if ShoppingCart.objects.filter(user=user).count() == 0:
            return Response(
                data={'error': 'Your shopping cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
