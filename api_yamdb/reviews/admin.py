from django.contrib import admin

from reviews.models import (
    Title,
    Genre,
    Category,
    Comment,
    Review,
    GenreTitle)


class GenreInline(admin.TabularInline):
    model = GenreTitle
    extra = 1


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category')  # ,'genre')
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'
    # inlines = [GenreInline, ]
    exclude = ['genre']


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('genre_id', 'title_id')
    ordering = ('-title_id',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'review_id', 'pub_date', 'author_id')
    search_fields = ('text',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title_id', 'author_id', 'text', 'score', 'pub_date')
