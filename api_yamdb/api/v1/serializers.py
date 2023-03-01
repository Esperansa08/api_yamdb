import datetime as dt
from django.contrib.auth import get_user_model
from django.core import validators
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from .exceptions import BadRating, IncorrectTitleInYear

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    slug = serializers.CharField(
        max_length=50,
        validators=[validators.validate_slug,
                    UniqueValidator(queryset=Genre.objects.all())])

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializerRead(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, required=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')


class TitleSerializerWrite(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(many=True,
                                         slug_field='slug',
                                         queryset=Genre.objects.all())

    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')

    def validate_year(self, value):
        year_now = dt.date.today().year
        print(year_now)
        if value > year_now:
            raise IncorrectTitleInYear('Передано некорректное значение года')
        return value 

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )

    def validate_score(self, value):
        if not (value in range(1, 11)):
            raise BadRating('Оценка должна быть в пределах от 1 до 10')
        return value

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class SignupSerializer(serializers.Serializer):
    username = serializers.RegexField(
        r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    email = serializers.EmailField(required=True, max_length=254)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не допустимо!'
            )
        return value


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = Review
        fields = ('username', 'confirmation_code')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
        read_only_fields = ('id', 'author', 'pub_date',)
