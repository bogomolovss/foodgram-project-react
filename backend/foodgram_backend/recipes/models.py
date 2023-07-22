from django.core.validators import MinValueValidator
from django.db import models
from ingredients.models import Ingredient
from tags.models import Tag
from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name="recipe",
        on_delete=models.CASCADE,
        verbose_name="Author"
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Name"
    )
    image = models.ImageField(
        upload_to="recipes/",
        default=None
    )
    text = models.TextField(verbose_name="Description")
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientAmount",
        verbose_name="Ingredients"
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Теги",
    )
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(
            1, message='Минимальное время приготовления 1 минута'
        )],
        verbose_name='Время приготовления')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredient_amount"
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(
            1, message='Минимальное кол-во = 1'
        )])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='Ingredient and Recipe in IngredientAmount is unique')
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite",
        verbose_name="User",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorite",
        verbose_name="Recipe"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='UserRecipe in favorite is unique')
        ]

    def __str__(self):
        return 'favorite'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="User"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="Recipe"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='UserRecipe in shopping cart is unique')
        ]

    def __str__(self):
        return 'shopping cart'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="User"
    )
    following = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='UserFollowing in following is unique')
        ]
