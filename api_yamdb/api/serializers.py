
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User

import datetime as dt
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, GenreTitle, Title

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):
    genre_name = serializers.CharField(source='name')

    class Meta:
        model = Genre
        fields = '__all__'
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, required=False, read_only=True)  
    #genre_detail = GenreSerializer(source='genre', read_only=True)
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ('name', 'year', 'description', 'category', 'genre')
        model = Title
        depth = 1

    def validate_year(self, value):
        year = dt.date.today().year
        if not (value <= year):
            raise serializers.ValidationError('Проверьте год выпуска!')
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

class SignupSerializer(serializers.Serializer):
    username = serializers.RegexField(
        r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    email = serializers.EmailField(required=True, max_length=254)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не допустимо!'
            )
        return value


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']
        model = User
        

class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(required=True)