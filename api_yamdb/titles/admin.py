from django.contrib import admin

from titles.models import Title, Genre, Category


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'pub_date', 'author')
    search_fields = ('name',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    search_fields = ('name', 'description')
    search_fields = ('name',)

@admin.register(Category)
class Categorydmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    search_fields = ('name',)
