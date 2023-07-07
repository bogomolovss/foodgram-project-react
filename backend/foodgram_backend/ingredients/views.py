from tags.mixins import ListRetrieveViewSet
from ingredients.models import Ingredient
from ingredients.serializers import IngredientSerializer


class TagViewset(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
