from rest_framework.filters import SearchFilter

from api.ingredients.serializers import IngredientSerializer
from api.mixins import ListRetrieveViewSet
from api.permissons import IsAdminOrReadOnly
from ingredients.models import Ingredient


class IngredientViewset(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)
