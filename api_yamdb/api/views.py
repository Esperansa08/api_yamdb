from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from django.shortcuts import get_object_or_404

from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User

from .serializers import (SignupSerializer, TokenSerializer)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Регистрация на Yamdb',
            message=f"Your confirmation code: {confirmation_code}",
            from_email=None,
            recipient_list=[user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )

    if default_token_generator.check_token(
        user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

