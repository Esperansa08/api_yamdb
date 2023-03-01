from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comment, Genre, Review, Title
from .exceptions import IncorrectAuthorReview, TitleOrReviewNotFound
from .filters import TitleFilter
from .permissions import (IsAdminOnly, IsAdminOrReadOnly,
                          IsAuthorModeratorAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignupSerializer,
                          TitleSerializerRead, TitleSerializerWrite,
                          TokenSerializer, UserSerializer)

User = get_user_model()


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
    confirmation_code = default_token_generator.make_token(user)
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
    permission_classes = (IsAdminOnly,)
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = (TitleSerializerRead, TitleSerializerWrite)
    filterset_class = TitleFilter
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category', 'genre__slug')

    def get_serializer_class(self):
        if self.action == 'list':
            return TitleSerializerRead
        return TitleSerializerWrite


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin, mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewCommentViewSet(viewsets.ModelViewSet):
    def get_title(self):
        title_id = self.kwargs.get("title_id")
        if not Title.objects.filter(pk=title_id).exists():
            raise TitleOrReviewNotFound(
                detail='Не найдено произведение или отзыв',
                code=status.HTTP_404_NOT_FOUND
            )
        return Title.objects.get(pk=title_id)


class ReviewViewSet(ReviewCommentViewSet):
    permission_classes = IsAuthorModeratorAdminOrReadOnly,
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_review(self):
        review_id = self.kwargs.get("pk")
        if not Review.objects.filter(pk=review_id).exists():
            raise TitleOrReviewNotFound(
                detail='Не найдено произведение или отзыв',
                code=status.HTTP_404_NOT_FOUND
            )
        return Review.objects.get(pk=review_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        author = self.request.user
        title = self.get_title()
        if title.reviews.filter(author=author).exists():
            raise IncorrectAuthorReview(
                'Этот автор уже оставлял отзыв к произведению')
        serializer.save(
            author=author,
            title=title
        )

    def get_patch_author(self):
        if self.request.method != 'PATCH':
            return self.request.user
        if not (self.request.user.is_moderator()
                or self.request.user.is_admin()):
            return self.request.user
        return self.get_review().author

    def perform_update(self, serializer):
        author = self.get_patch_author()
        title = self.get_title()
        serializer.save(
            author=author,
            title=title
        )


class CommentViewSet(ReviewCommentViewSet):
    permission_classes = IsAuthorModeratorAdminOrReadOnly,
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_review(self):
        review_id = self.kwargs.get("review_id")
        print(self.kwargs)
        if not Review.objects.filter(pk=review_id).exists():
            raise TitleOrReviewNotFound(
                detail='Не найдено произведение или отзыв',
                code=status.HTTP_404_NOT_FOUND
            )
        return Review.objects.get(pk=review_id)

    def get_queryset(self):
        return self.get_review().comments.all()

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
