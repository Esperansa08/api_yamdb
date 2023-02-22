from django.urls import include, path


from api.views import (token, signup)


urlpatterns = [
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', token, name='token')
]
