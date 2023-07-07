from django.db import models

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
        upload_to="cats/images/",
        null=True,
        default=None
    )
    description = models.TextField(verbose_name="Description")
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Теги",
    )
