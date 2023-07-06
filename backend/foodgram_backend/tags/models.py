from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        verbose_name="Tag"
    )
    color = models.CharField(
        null=True,
        blank=True,
        max_length=7,
        verbose_name="Color")
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Slug"
    )
