import datetime as dt

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_year(value):
    if value > dt.date.today().year:
        raise ValidationError(_('указанный %(value)s год, больше текущего'),
                              params={'value': value}, )
