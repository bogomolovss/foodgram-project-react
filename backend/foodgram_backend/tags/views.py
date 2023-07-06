from .mixins import ListRetrieveViewSet
from .models import Tag
from .serializers import TagSerializer


class TagViewset(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
