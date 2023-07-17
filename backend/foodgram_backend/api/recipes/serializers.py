import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from api.tags.serializers import TagSerializer
from recipes.models import (
    Follow, IngredientAmount, Recipe, Ingredient, Tag
)
from api.users.serializers import CustomUserSerializer
from rest_framework.validators import UniqueTogetherValidator


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [
            UniqueTogetherValidator(
                queryset=IngredientAmount.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        source='ingredient_amount',
        many=True,
        read_only=True
    )

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'is_in_shopping_cart',
            'author', 'name',
            'image', 'text',
            'ingredients', 'tags',
            'cooking_time', 'is_favorited',
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favorite__user=user, id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(
            cart__user=user,
            id=obj.id
        ).exists()

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Need at least one ingredient for recipe'})
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(Ingredient,
                                           id=ingredient_item['id'])
            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    'Ingredients must be unique!'
                )
            ingredient_list.append(ingredient)
            if int(ingredient_item['amount']) < 0:
                raise serializers.ValidationError({
                    'ingredients': (
                        'Ingredient amount must be more than zero!'
                    )})
        data['ingredients'] = ingredients
        return data

    def create(self, validated_data):
        #
        user = self.context.get('request').user
        # Уберем список ингредиентов из словаря validated_data и сохраним его
        print(validated_data)
        ingredients = validated_data.pop('ingredients')
        # Создадим новый рецепт без ингредиентов
        recipe = Recipe.objects.create(**validated_data, author=user)

        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        # Для каждого ингредиента из списка ингредиентов
        for ingredient in ingredients:
            IngredientAmount.objects.create(
                ingredient_id=ingredient.get('id'),
                recipe=recipe,
                amount=ingredient.get('amount')
            )
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)

        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        IngredientAmount.objects.filter(recipe=instance).all().delete()
        for ingredient in validated_data.get('ingredients'):
            IngredientAmount.objects.create(
                ingredient_id=ingredient.get('id'),
                recipe=instance,
                amount=ingredient.get('amount')
            )
        instance.save()
        return instance


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user', 'following')


class RecipeSerializerLite(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
