from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    class Role(models.TextChoices):
        USER = 'user', _('Пользователь')
        ADMIN = 'admin', _('Администратор')
        MODERATOR = 'moderator', _('Модератор')

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
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
        verbose_name='Права доступа'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def is_upperclass(self):
        return self.role in {
            self.Role.USER,
            self.Role.ADMIN,
            self.Role.MODERATOR,
        }

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.Role.USER

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR
