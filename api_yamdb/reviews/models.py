from django.db import models

from users.models import User


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Название жанра')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        default='dsffsd',
        verbose_name='Жанр')

    class Meta:
        verbose_name_plural = 'Жанры'
        verbose_name = 'Жанр'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(
        max_length=256,
        verbose_name='название произведения',
        help_text='Введите название произведения')
    year = models.IntegerField(default=2023,
                               verbose_name='год публикации',
                               help_text='Введите год публикации произведения')
    genre = models.ManyToManyField(
        'Genre',
        related_name='genres',
        through='GenreTitle')
    category = models.ForeignKey(
        'Category',
        blank=True,
        null=True,
        db_column='category',
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория произведения',
        help_text='Категория, к которой относиться произведение')
    description = models.TextField(
        default='описание',
        null=True,
        verbose_name='Описание')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name[:15]


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


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Жанр-произведение'
        verbose_name_plural = 'Жанр-произведение'

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Отзыв на произведение',
    )
    text = models.TextField(
        'Текст отзыва',
        help_text='Введите текст отзыва',
    )
    author = models.ForeignKey(
        User,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации отзыва',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        unique_together = ('title', 'author',)
        ordering = ('-pub_date',)
        verbose_name_plural = 'Отзывов'
        verbose_name = 'Отзывы'


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        null=False,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,)
    review = models.ForeignKey(
        Review,
        related_name='comments',
        null=False,
        verbose_name='Комментируемый отзыв',
        on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления комментария',
        auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарии'
