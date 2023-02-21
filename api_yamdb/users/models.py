from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator')
    ]
    username = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    role = models.SlugField(
        choices=ROLES,
        default=USER,
        verbose_name='Права доступа'
    )
    confirmation_code = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Код подтверждения авторизации'
    )

    class Meta:
        ordering = ['id']

