from rest_framework import viewsets
from recipes.models import Recipe, Favorite, ShoppingCart
from api.recipes.serializers import RecipeSerializer, FollowSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status


class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, id):
        user = request.user
        recipe = Recipe.objects.filter(id=id)
        if not recipe.exists():
            return Response(
                data={'error': 'Recipe by this id not exist!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    data={'error': 'This recipe already in favorite!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        Favorite.objects.create(user=user, recipe=recipe)
        serializer = RecipeSerializer(recipe)
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


class FollowViewset(viewsets.ModelViewSet):
    serializer_class = FollowSerializer

    def perform_create(self, serializer: FollowSerializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.request.user.follower.all()
