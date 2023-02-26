import datetime as dt

from django.db.models import Avg

from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, GenreTitle, Title, Review

from users.models import User
from api.exceptions import (BadRating, TitleOrReviewNotFound,
                            IncorrectGenresInData)


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не допустимо')
        return value

    class Meta:
        fields = ('username', 'email')
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    slug = serializers.CharField()

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, required=False)
    # genre_detail = GenreSerializer(source='genre', read_only=True)
    category = serializers.StringRelatedField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'rating', 'category', 'genre')

    def get_fields(self):
        fields = super().get_fields()

        exclude_fields = self.context.get('exclude_fields', [])
        for field in exclude_fields:
            fields.pop(field, default=None)

        return fields

    def validate_year(self, value):
        year = dt.date.today().year
        if not (value <= year):
            raise TitleOrReviewNotFound
        return value

    def get_rating(self, obj):
        print(self)
        return Review.objects.filter(
            title=obj).aggregate(Avg('score'))['score__avg']

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            title = Title.objects.create(**validated_data)
            return title
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)

        for genre in genres:
            genre_slug = genre['slug']
            current_genre = Genre.objects.filter(slug=genre_slug)
            if len(current_genre) != 1:
                raise IncorrectGenresInData()
            GenreTitle.objects.create(genre=current_genre[0], title=title)
        return title

    # def update(self, validated_data):
    #     if 'genre' not in self.initial_data:
    #         title = Title.objects.create(**validated_data)
    #         return title
    #     genres = validated_data.pop('genre')
    #     title = Title.objects.create(**validated_data)

    #     for genre in genres:
    #         current_genre,status = Genre.objects.get_or_create(**genre)
    #         GenreTitle.objects.create(genre=current_genre, title=title)
    #     return title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
        lookup_field = 'slug'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )

    def validate_score(self, value):
        if not (value in range(1, 11)):
            raise BadRating()
        return value

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
        read_only_fields = ('id', 'author', 'pub_date',)
