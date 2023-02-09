import datetime

from django.core.exceptions import ValidationError


def validate_title_year(value):
    current_year = datetime.datetime.now().year
    if value > current_year:
        raise ValidationError(
            'Передаваемый год не может быть больше текущего'
        )
