from rest_framework import viewsets
from recipes.models import Recipe
from api.recipes.serializers import RecipeSerializer, FollowSerializer


class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class FollowViewset(viewsets.ModelViewSet):
    serializer_class = FollowSerializer

    def perform_create(self, serializer: FollowSerializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.request.user.follower.all()
