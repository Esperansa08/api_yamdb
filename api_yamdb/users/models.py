from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'
ROLES = [
    (USER, 'Пользователь'),
    (ADMIN, 'Администратор'),
    (MODERATOR, 'Модератор')
]


class User(AbstractUser):
    
    username = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя',
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
    
    def is_admin(self):
        return (
            self.role == ADMIN
            or self.is_staff
        )

    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username


    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
