from django.urls import path, include
from rest_framework import routers

from api.views import TitleViewSet, GenreViewSet, CategoryViewSet

v1_router = routers.DefaultRouter()
v1_router.register('titles', TitleViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('categories', CategoryViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
