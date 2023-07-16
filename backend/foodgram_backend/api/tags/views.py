from api.mixins import ListRetrieveViewSet
from tags.models import Tag
from api.tags.serializers import TagSerializer
from api.permissons import IsAdminOrReadOnly


class TagViewset(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
