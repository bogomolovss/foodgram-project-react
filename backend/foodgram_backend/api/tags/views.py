from api.mixins import ListRetrieveViewSet
from api.permissons import IsAdminOrReadOnly
from api.tags.serializers import TagSerializer
from tags.models import Tag


class TagViewset(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
