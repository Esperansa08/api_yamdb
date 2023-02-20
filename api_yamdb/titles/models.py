from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Title(models.Model):
    name = models.TextField(
        verbose_name='название произведения',
        help_text='Введите название произведения')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Автор произведения',
        help_text='Автор из таблицы User')
    genre = models.ForeignKey(
        'Genre',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Жанр произведения',
        help_text='Жанр, к которой относиться произведение')
    category = models.ForeignKey(
        'Category',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория произведения',
        help_text='Категория, к которой относиться произведение')
    # image = models.ImageField(
    #     verbose_name='Картинка',
    #     upload_to='titles/',
    #     null=True,
    #     blank=True)

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.text[:15]
    
class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название жанра')
    slug = models.SlugField(unique=True, verbose_name='Жанр')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name_plural = 'Жанр'
        verbose_name = 'Жанр'

    def __str__(self):
        return self.title
        
class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название категории')
    slug = models.SlugField(unique=True, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name_plural = 'Категория'
        verbose_name = 'Категории'

    def __str__(self):
        return self.title