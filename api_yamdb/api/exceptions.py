from rest_framework import status
from rest_framework.serializers import ValidationError


class TitleOrReviewNotFound(ValidationError):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Не найдено произведение или отзыв'


class BadRating(ValidationError):
    default_detail = 'Оценка должна быть в пределах от 1 до 10'
