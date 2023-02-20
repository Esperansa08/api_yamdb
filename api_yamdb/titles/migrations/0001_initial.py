# Generated by Django 3.2 on 2023-02-20 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название категории')),
                ('slug', models.SlugField(unique=True, verbose_name='Категория')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Категории',
                'verbose_name_plural': 'Категория',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название жанра')),
                ('slug', models.SlugField(unique=True, verbose_name='Жанр')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанр',
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(help_text='Введите название произведения', verbose_name='название произведения')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(help_text='Автор из таблицы User', on_delete=django.db.models.deletion.CASCADE, related_name='titles', to=settings.AUTH_USER_MODEL, verbose_name='Автор произведения')),
                ('category', models.ForeignKey(blank=True, help_text='Категория, к которой относиться произведение', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='titles.category', verbose_name='Категория произведения')),
                ('genre', models.ForeignKey(blank=True, help_text='Жанр, к которой относиться произведение', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='titles.genre', verbose_name='Жанр произведения')),
            ],
            options={
                'verbose_name': 'произведение',
                'verbose_name_plural': 'Произведения',
            },
        ),
    ]
