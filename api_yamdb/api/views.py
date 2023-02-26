
from django.db.models import Avg
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from rest_framework import permissions, status, viewsets, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.serializers import ValidationError

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from api.permissions import isAdminOnly
from api.serializers import (
    GenreSerializer,
    TitleSerializerRead,
    TitleSerializerWrite,
    CategorySerializer,
    SignupSerializer,
    TokenSerializer,
    ReviewSerializer,
    CommentSerializer,
    UserSerializer)
from api.exceptions import TitleOrReviewNotFound
from reviews.models import Category, Comment, Genre, Review, Title

@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    """Содаем пользователя и получаем письмо с ключом на почту"""
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    try:
        user, created = User.objects.get_or_create(
            username=username,
            email=email.lower()
        )
    except IntegrityError:
        return Response(
            {'message': 'Имя пользователя или почта уже используются.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code  = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация на Yamdb',
        message=f"Your confirmation code: {confirmation_code}",
        from_email=None,
        recipient_list=[user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def token(request):
    "Проверяем полученый ключ и выдаем токен Brearer"
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    token = serializer.validated_data['confirmation_code']
    if not default_token_generator.check_token(user, token):
        return Response(
            'Неверный код подтверждения', status=status.HTTP_400_BAD_REQUEST
        )
    refresh = str(RefreshToken.for_user(user).access_token)
    return Response(
        {"token": refresh},
        status=status.HTTP_200_OK)


@api_view(['GET', 'PATCH'])
@permission_classes((IsAuthenticated,))
def users_me(request):
    """Получаем и обновляем свои данные"""
    user = request.user
    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "PATCH":
        serializer = UserSerializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (isAdminOnly,)
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)



class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = (TitleSerializerRead, TitleSerializerWrite)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category',)  # 'genres')

    def get_serializer_class(self):
        if self.action == 'list':
            return TitleSerializerRead
        return TitleSerializerWrite

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action not in ('list', 'retrieve'):
            context['exclude_fields'] = ['rating']
        return context


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewCommentViewSet(viewsets.ModelViewSet):
    def get_title(self):
        title_id = self.kwargs.get("title_id")
        if not Title.objects.filter(pk=title_id).exists():
            raise TitleOrReviewNotFound
        return Title.objects.get(pk=title_id)

    def get_review(self):
        review_id = self.kwargs.get("review_id")
        if not Review.objects.filter(pk=review_id).exists():
            raise TitleOrReviewNotFound
        return Review.objects.get(pk=review_id)


class ReviewViewSet(ReviewCommentViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def update_rating(self):
        title = self.get_title()
        rating = Review.objects.filter(
            title=title).aggregate(rating=Avg('score'))
        title.rating = rating['rating']
        title.save()

    def get_queryset(self):
        return Review.objects.filter(title=self.get_title())

    def perform_create(self, serializer):
        author = self.request.user
        title = self.get_title()
        if Review.objects.filter(
                title=title, author=author).exists():
            raise ValidationError(
                'Этот автор уже оставлял отзыв к произведению')
        serializer.save(
            author=author,
            title=title
        )
        self.update_rating()

    def perform_update(self, serializer):
        author = self.request.user
        title = self.get_title()
        serializer.save(
            author=author,
            title=title
        )
        self.update_rating()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self.update_rating()


class CommentViewSet(ReviewCommentViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(review=self.get_review())

    def perform_create(self, serializer):
        author = self.request.user
        self.get_title()
        review = self.get_review()
        serializer.save(
            author=author,
            review=review
        )

    def perform_update(self, serializer):
        author = self.request.user
        self.get_title()
        review = self.get_review()
        serializer.save(
            author=author,
            review=review
        )
