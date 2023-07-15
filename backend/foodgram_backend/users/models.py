from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(
        max_length=50,
        blank=False,
        verbose_name="name",
        null=False
    )

    second_name = models.CharField(
        max_length=50,
        blank=False,
        verbose_name='surname',
        null=False
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
        null=False,
        blank=False,
        verbose_name='email'
    )

    username = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True,
        verbose_name='username'
    )
