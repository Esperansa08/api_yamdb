from reviews.models import Title
from django_filters.rest_framework import BaseInFilter, CharFilter, FilterSet


class CharFilterInFilter(BaseInFilter, CharFilter):
    pass


class TitleFilter(FilterSet):
    genre = CharFilterInFilter(field_name='genre__slug', )
    category = CharFilterInFilter(field_name='category__slug',)
    name = CharFilterInFilter(
        field_name='name',
        lookup_expr='in',)
    class Meta:
        model = Title
        fields = ('genre', 'category', 'year', 'name',)
