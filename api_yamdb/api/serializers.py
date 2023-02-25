import datetime as dt

from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Title, Review

from users.models import User
from api.exceptions import BadRating, TitleOrReviewNotFound


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
    genre_name = serializers.CharField(source='name')

    class Meta:
        model = Genre
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, required=False, read_only=True)
    genre_detail = GenreSerializer(source='genre', read_only=True)
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('name', 'year', 'description', 'category', 'genre')
        model = Title
        depth = 1

    def validate_year(self, value):
        year = dt.date.today().year
        if not (value <= year):
            raise TitleOrReviewNotFound
        return value

    # def create(self, validated_data):
    #     if 'genre' not in self.initial_data:
    #         title = Title.objects.create(**validated_data)
    #         return title
    #     genres = validated_data.pop('genre')
    #     title = Title.objects.create(**validated_data)

    #     for genre in genres:
    #         current_genre,status = Genre.objects.get_or_create(**genre)
    #         GenreTitle.objects.create(genre=current_genre, title=title)
    #     return title

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
