from ingredients.models import Ingredient
from api.ingredients.serializers import IngredientSerializer
from api.mixins import ListRetrieveViewSet
from api.permissons import IsAdminOrReadOnly


class IngredientViewset(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
