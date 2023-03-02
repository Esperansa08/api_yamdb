from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg, OuterRef
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comment, Genre, Review, Title
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
    token = AccessToken.for_user(user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdminOnly,)
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        """Получаем и обновляем свои данные"""
        user = request.user
        if request.method == 'PATCH':
            serializer = UserSerializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = (TitleSerializerRead, TitleSerializerWrite)
    filterset_class = TitleFilter
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        return Title.objects.annotate(
            rating=Review.objects.filter(
                title=OuterRef('pk')).values(
                    'title_id').annotate(Avg('score')).values('score__avg')
        )

    def get_serializer_class(self):
        if self.request.method == 'GET':
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


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = IsAuthorModeratorAdminOrReadOnly,
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_patch_author(self):
        if self.request.method != 'PATCH':
            return self.request.user
        if not (self.request.user.is_moderator
                or self.request.user.is_admin):
            return self.request.user
        return self.get_review().author

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get("title_id"))

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get("pk"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        author = self.get_patch_author()
        title = self.get_title()
        serializer.save(
            author=author,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = IsAuthorModeratorAdminOrReadOnly,
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_patch_author(self):
        if self.request.method != 'PATCH':
            return self.request.user
        if not (self.request.user.is_moderator
                or self.request.user.is_admin):
            return self.request.user
        return self.get_review().author

    def get_review(self):
        return get_object_or_404(Review,
                                 pk=self.kwargs.get("review_id"),
                                 title=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        author = self.get_patch_author()
        review = self.get_review()
        serializer.save(
            author=author,
            review=review
        )
