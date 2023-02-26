from django.urls import include, path
from rest_framework import routers

from api.views import (token, signup, users_me, TitleViewSet, GenreViewSet,
                       CategoryViewSet, UserViewSet, ReviewViewSet, CommentViewSet)

v1_router = routers.DefaultRouter()
v1_router.register('titles', TitleViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register(r'users', UserViewSet, basename='user')

v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    viewset=ReviewViewSet
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    viewset=CommentViewSet)

urlpatterns = [
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', token, name='token'),
    path('v1/users/me/', users_me),
    path('v1/', include(v1_router.urls)),
]
