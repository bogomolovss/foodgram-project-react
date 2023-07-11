from rest_framework import viewsets
from recipes.models import Recipe
from api.recipes.serializers import RecipeSerializer


class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
