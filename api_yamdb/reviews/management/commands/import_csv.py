import logging
from csv import DictReader
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Title, Review, GenreTitle
from users.models import User

MESSAGE = 'Данные успешно загружены в таблицу'
SUCCESS_MESSAGE = 'Все данные успешно загружены'


logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    filemode='w'
)


class Command(BaseCommand):
    help = 'Команда для создания БД на основе имеющихся csv файлов'

    def genre_create(row):
        Genre.objects.create(
            id=row['id'],
            name=row['name'],
            slug=row['slug'])

    def category_create(row):
        Category.objects.create(
            id=row['id'],
            name=row['name'],
            slug=row['slug'])

    def title_create(row):
        Title.objects.create(
            id=row['id'],
            name=row['name'],
            year=row['year'],
            category=Category.objects.get(id=row['category']))

    def genre_title_create(row):
        GenreTitle.objects.create(
            id=row['id'],
            title_id=row['title_id'],
            genre_id=row['genre_id'])

    def user_create(row):
        User.objects.create(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            role=row['role'],
            bio=row['bio'],
            first_name=row['first_name'],
            last_name=row['last_name'])

    def comment_create(row):
        Comment.objects.create(
            id=row['id'],
            review_id=row['review_id'],
            text=row['text'],
            author_id=row['author'],
            pub_date=row['pub_date'])

    def review_create(row):
        Review.objects.create(
            id=row['id'],
            text=row['text'],
            title_id=row['title_id'],
            author_id=row['author'],
            score=row['score'],
            pub_date=row['pub_date'])

    ACTIONS = [
        (user_create, User, 'users.csv'),
        (category_create, Category, 'category.csv'),
        (genre_create, Genre, 'genre.csv'),
        (title_create, Title, 'titles.csv'),
        (genre_title_create, GenreTitle, 'genre_title.csv'),
        (review_create, Review, 'review.csv'),
        (comment_create, Comment, 'comments.csv'),
    ]

    def handle(self, *args, **options):
        logging.info('Загрузка данных из csv в базу:')
        for func, model, file in self.ACTIONS:
            if model.objects.exists():
                logging.info('Таблица уже содержит данные.')
            for row in DictReader(
                open(
                    f'static/data/{file}',
                    encoding='utf8')):
                func(row)
            logging.info(MESSAGE)
        logging.info(SUCCESS_MESSAGE)
