from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    USER_ROLE = 'user'
    MODERATOR_ROLE = 'moderator'
    ADMIN_ROLE = 'admin'

    CHOICES_ROLE = (
        (USER_ROLE, 'user'),
        (MODERATOR_ROLE, 'moderator'),
        (ADMIN_ROLE, 'admin')
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(UnicodeUsernameValidator(),)
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=16,
        choices=CHOICES_ROLE,
        default=USER_ROLE,
        blank=True,
        null=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=255,
        blank=True,
        null=True
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN_ROLE

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR_ROLE

    @property
    def is_user(self):
        return self.role == self.USER_ROLE

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}'
