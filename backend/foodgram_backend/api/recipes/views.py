from rest_framework import viewsets
from recipes.models import Recipe
from api.recipes.serializers import RecipeSerializer, FollowSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    # @action(
    #     methods=['POST', 'PATCH'],
    #     detail=True,
    # )
    # def favorite(self, request):
    #     user = request.user
    #     if request.method == 'GET':

    #     pass


class FollowViewset(viewsets.ModelViewSet):
    serializer_class = FollowSerializer

    def perform_create(self, serializer: FollowSerializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.request.user.follower.all()
