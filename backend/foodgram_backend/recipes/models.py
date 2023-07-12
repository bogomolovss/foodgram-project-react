from django.db import models
from django.core.validators import MinValueValidator
from tags.models import Tag
from users.models import User
from ingredients.models import Ingredient


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
        null=True,
        default=None,
        blank=True
    )
    description = models.TextField(verbose_name="Description")
    ingredients = models.ManyToManyField(
        Ingredient,
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


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite",
        verbose_name="User",
    ),
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
        unique_together = ('user', 'following',)
