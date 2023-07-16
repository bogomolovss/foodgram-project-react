from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.ingredients.views import IngredientViewset
from api.recipes.views import RecipeViewset
from api.tags.views import TagViewset
from api.users.views import CustomUserViewSet

router = DefaultRouter()

router.register(
    prefix=r'tags',
    viewset=TagViewset,
    basename='tag'
)
router.register(
    prefix=r'ingredients',
    viewset=IngredientViewset,
    basename='ingredient'
)
router.register(
    prefix=r'recipes',
    viewset=RecipeViewset,
    basename='recipe'
)
router.register('users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
