from django.urls import include, path
from rest_framework import routers

from api.views import (token, signup, TitleViewSet, GenreViewSet, CategoryViewSet)

v1_router = routers.DefaultRouter()
v1_router.register('titles', TitleViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('categories', CategoryViewSet)

urlpatterns = [
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', token, name='token'),
    path('v1/', include(v1_router.urls)),
]
