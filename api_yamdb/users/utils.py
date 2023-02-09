from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import EMAIL_HOST_USER


def create_confirmation_code(user):
    return default_token_generator.make_token(user)


def send_confirmation_code(user):
    send_mail(
        subject=f'Подтверждение авторизации пользователя {user.username}',
        message=(f'Добрый день, {user.username}! Для того, чтобы завершить '
                 'регистрацию Вам необходимо отправить запрос на адрес '
                 f'api/v1/auth/token/ с username: {user.username} и с '
                 f'кодом: {user.confirmation_code}'),
        from_email=EMAIL_HOST_USER,
        recipient_list=[user.email]
    )


def create_jwt_token(user):
    return str(RefreshToken.for_user(user).access_token)
