from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Title(models.Model):
    name = models.TextField(
        max_length=256,
        verbose_name='название произведения',
        help_text='Введите название произведения')
    year = models.IntegerField(default=2023,
        verbose_name='год публикации',
        help_text='Введите год публикации произведения')
    description = models.TextField(default='описание',verbose_name='Описание')
    genre = models.ForeignKey(
        'Genre',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Жанр произведения',
        help_text='Жанр, к которой относиться произведение')
    category =  models.ForeignKey(
        'Category',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория произведения',
        help_text='Категория, к которой относиться произведение')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name[:15]
    
class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Жанр')

    class Meta:
        verbose_name_plural = 'Жанры'
        verbose_name = 'Жанр'

    def __str__(self):
        return self.name
        
class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Категория')

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категории'

    def __str__(self):
        return self.name
