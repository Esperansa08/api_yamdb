import datetime as dt

from django.db.models import Avg
from rest_framework import viewsets
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
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializerRead(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, required = False)
    rating = serializers.SerializerMethodField(read_only=True)
 
    class Meta:
        model = Title
        fields = ['id', 'name', 'year', 'rating', 'description', 'genre',
                  'category']
 
    def get_rating(self, obj):
        return Review.objects.filter(
            title=obj).aggregate(Avg('score'))['score__avg']
 
 
class TitleSerializerWrite(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(many=True,
                                         slug_field='slug',
                                         queryset=Genre.objects.all())


    rating = serializers.SerializerMethodField(read_only=True)
 
    class Meta:
        model = Title
        fields = ['id', 'name', 'year', 'rating', 'description', 'genre',
                  'category']
 
    def get_rating(self, obj):
        return Review.objects.filter(
            title=obj).aggregate(Avg('score'))['score__avg']
            
    def to_representation(self, instance):
        request = self.context.get ('request')
        context = {'request': request}
        return TitleSerializerRead(instance, context=context).data   
        
        
class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    #permission_classes = [IsAdminOrReadOnly, ]
 
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializerRead
        return TitleSerializerWrite
 
    def perform_create(self, serializer):
        category_slug = self.request.data['category']
        genre = self.request.data['genre']
        category = get_object_or_404(Category, slug=category_slug)
        genres = []
        for item in genre:
            genres.append(get_object_or_404(Genre, slug=item))
        serializer.save(category=category, genres=genres)
 

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

