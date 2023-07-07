from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tags.views import TagViewset

router = DefaultRouter()

router.register(
    prefix=r'tags',
    viewset=TagViewset,
    basename='tag'
)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
