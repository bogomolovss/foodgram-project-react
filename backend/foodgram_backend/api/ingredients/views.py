from ingredients.models import Ingredient
from api.ingredients.serializers import IngredientSerializer
from api.mixins import ListRetrieveViewSet


class IngredientViewset(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
