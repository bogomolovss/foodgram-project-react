from api.filters import RecipeFilter
from api.pagination import CustomPageNumberPagination
from api.permissons import IsAuthorOrReadOnlyPermission
from api.recipes.serializers import RecipeSerializer, RecipeSerializerLite
from django.http import FileResponse
from django_filters import rest_framework as filters
from recipes.models import Favorite, IngredientAmount, Recipe, ShoppingCart
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = CustomPageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter
    filterset_fields = (
        'tags', 'author', 'is_favorited', 'is_in_shopping_cart'
    )

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        return self.post_or_delete_entity(Favorite, request, pk)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        return self.post_or_delete_entity(ShoppingCart, request, pk)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        shopping_list = {}
        ingredients = IngredientAmount.objects.filter(
            recipe__cart__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount')
        for item in ingredients:
            name = item[0]
            if name not in shopping_list:
                shopping_list[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                shopping_list[name]['amount'] += item[2]
        file_content = []
        for x in enumerate(shopping_list.items()):
            amount = x[1][1].get('amount')
            measurement_unit = x[1][1].get('measurement_unit')
            file_content.append(
                f'{x[0]+1} - {x[1][0]} - {amount}{measurement_unit}\n'
            )
        response = FileResponse(
            file_content,
            content_type='text/plain; charset=UTF-8'
        )
        response['Content-Disposition'] = (
            'attachment; filename="{file}.txt"')
        return response

    # universal method for post/delete Favorite or ShoppingCart object
    def post_or_delete_entity(self, model, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if model.objects.filter(user=user, recipe__id=pk).exists():
                return Response(
                    data={
                        'error': f'This recipe already in {model.__name__}!'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            model.objects.create(user=user, recipe=recipe)
            serializer = RecipeSerializerLite(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # DELETE
        entity = model.objects.filter(user=user, recipe=recipe)
        if not entity.exists():
            return Response(
                data={'error': f'This recipe not in your {model.__name__}!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        entity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
