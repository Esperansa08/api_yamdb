from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination

from api.serializers import (TitleSerializer, GenreSerializer,
                             CategorySerializer)
#from api.permissions import IsAuthorOrReadOnly
from titles.models import Title, Genre, Category


class TitleViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly)
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    #pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
