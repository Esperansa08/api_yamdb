import datetime as dt
from rest_framework import viewsets
import sys
sys.setrecursionlimit(2000)
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
# from rest_framework.exceptions import ValidationError
# from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Title, Review, GenreTitle

from users.models import User


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
        lookup_field = 'slug'
        # extra_kwargs = {
        #     'name': {'validators': []},
        # }

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, required = False)

    #genre = serializers.SlugRelatedField(
    #    slug_field='slug', many=True, queryset=Genre.objects.all())

    category = CategorySerializer(read_only= True)
    #category = serializers.StringRelatedField()
    # category = serializers.SlugRelatedField(
    #     slug_field='slug', queryset=Category.objects.all()
    # )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'rating', 'category', 'genre')
        model = Title

    # def get_fields(self):
    #     fields = super().get_fields()

    #     exclude_fields = self.context.get('exclude_fields', [])
    #     for field in exclude_fields:
    #         fields.pop(field, default=None)

    #     return fields
   
    def validate_year(self, value):
        year = dt.date.today().year
        if not (value <= year):
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value

    def get_rating(self, obj):
        #print(self)
        return Review.objects.filter(
            title=obj).aggregate(Avg('score'))['score__avg']

#     def to_representation(self, obj):
#        # print(obj.genre.name)
#         return {
#             'id': obj.id,
#             'name': obj.name,
#             'year': obj.year,
#             'rating': None,
#             'description': obj.description,
#             'category': {'name': f'{obj.category.name}',
#                          'slug': f'{obj.category.slug}'},
#             'genres': [({'name': f'{genre.name}',
#                          'slug': f'{genre.slug}'}) for genre in
#                        obj.genres.all()
#                        ]
#         }
    
    
    
    # def to_representation(self, instance):
    #     data = super(TitleSerializer, self).to_representation(instance)
    #     #data.update(...)
    #     request = self.context.get ('request')
    #     context = {'request': request}
    #     return data
    
    # def create(self, validated_data):
    #     if 'genre' not in self.initial_data:
    #         title = Title.objects.create(**validated_data)
    #         return title
    #     genres = validated_data.pop('genre')
    #     title = Title.objects.create(**validated_data)

    #     for genre in genres:
    #         genre_slug = genre['slug']
    #         current_genre = Genre.objects.filter(slug=genre_slug)
    #         if len(current_genre) != 1:
    #             raise serializers.ValidationError('Проверьте жанр!')
    #         GenreTitle.objects.create(genre=current_genre[0], title=title)
    #     return title


    # def get(self):
    #     genre = GenreSerializer(many=True)
    #     return genre
    

    # def update(self, instance, validated_data):
    #     for attr, value in validated_data.items():
    #         if not getattr(instance, attr):
    #             setattr(instance, attr, value)
    #     instance.save()
    #     return instance

   
    # def create(self, validated_data):
    #     if 'genre' not in self.initial_data:
    #         title = Title.objects.create(**validated_data)
    #         return title

    #     genres = validated_data.pop('genre')
    #     title = Title.objects.create(**validated_data)

    #     for genre in genres:
    #         current_genre, status = Title.objects.get(**genre)
    #         GenreTitle.objects.create(genre=current_genre, title=title)
    #     return title
class TitleSerializerRead(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, required = False,)
    rating = serializers.SerializerMethodField(read_only=True)
 
    class Meta:
        model = Title
        fields = ['id', 'name', 'year', 'rating', 'description', 'genre',
                  'category']
 
    def get_rating(self, obj):
        return Review.objects.filter(
            title=obj).aggregate(Avg('score'))['score__avg']
 
    # def to_representation(self, obj):

    #     return {
    #         'id': obj.id,
    #         'name': obj.name,
    #         'year': obj.year,
    #         'rating': None,
    #         'description': obj.description,
    #         'category': {'name': f'{obj.category.name}',
    #                      'slug': f'{obj.category.slug}'},
    #         'genres': [({'name': f'{genre.name}',
    #                      'slug': f'{genre.slug}'}) for genre in
    #                    obj.genres.all()
    #                    ]
    #     }
 
class TitleSerializerWrite(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug', many=True,
                                            queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(#source='genres',
                                          many=True,
                                         slug_field='slug',
                                         queryset=Genre.objects.all())
    
    #genre = serializers.SlugRelatedField(
#         slug_field='slug', many=True, queryset=Genre.objects.all())

#     #category = CategorySerializer(read_only= True)
#     #category = serializers.StringRelatedField()
#     category = serializers.SlugRelatedField(
#         slug_field='slug', queryset=Category.objects.all()
#     )


    rating = serializers.SerializerMethodField(read_only=True)
 
    class Meta:
        model = Title
        fields = ['id', 'name', 'year', 'rating', 'description', 'genre',
                  'category']
 
    def get_rating(self, obj):
        return Review.objects.filter(
            title=obj).aggregate(Avg('score'))['score__avg']
        
        
        
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
 



# class TitleSerializerPostPut(serializers.ModelSerializer):
#     category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())
#     genre = serializers.SlugRelatedField(source='genres', many=True,
#                                          slug_field='slug', queryset=Genre.objects.all())
#     #rating = serializers.SerializerMethodField(read_only=True)
 
#     class Meta:
#         model = Title
#         fields = ['id', 'name', 'year', 'rating', 'description', 'genre',
#                   'category']
 
#     def get_rating(self, obj):
#         #print(self)
#         return Review.objects.filter(
#             title=obj).aggregate(Avg('score'))['score__avg']
    
    
    
    # def get_rating(self, obj):
    #     score_avg = \
    #         Review.objects.filter(title_id=obj.id).aggregate(Avg('score'))[
    #             'score__avg']
    #     if score_avg is None:
    #         return None
    #     return int(score_avg)    


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    # title = serializers.SlugRelatedField(
    #     slug_field='name',
    #     queryset=Title.objects.all(),
    #     default=1
    # )

    def validate_score(self, value):
        if not (value in range(1, 10)):
            raise serializers.ValidationError(
                'Оценка должна быть в пределах от 1 до 10')
        return value

    def validate_title(self, value):
        return Title.objects.get(
            pk=self.context['view'].kwargs.get("title_id"))

    class Meta:
        model = Review
        fields = ('id',  'text', 'author', 'score', 'pub_date') #'title',
        read_only_fields = ('title',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"
