import base64

from rest_framework import serializers
from django.core.files.base import ContentFile
from recipes.models import Recipe

from api.tags.serializers import TagSerializer
from api.ingredients.serializers import IngredientSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'author', 'name', 'image',
            'description', 'ingredients', 'tags', 'cooking_time'
        )
