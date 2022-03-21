from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта',
        help_text='Адрес электронной почты пользователя'
    )
    username = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Псевдоним',
        help_text='Псевдоним пользователя'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
        help_text='Биография пользователя'
    )
    role = models.CharField(
        max_length=10,
        choices=ROLES,
        default=USER,
        verbose_name='Роль',
        help_text='Административная роль пользователя'
    )
    confirmation_code = models.CharField(
        max_length=10,
        default=get_random_string(length=15),
        editable=False,
        verbose_name='Код подтверждения',
        help_text='UUID код подтверждения для получения токена'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя',
        help_text='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия',
        help_text='Фамилия пользователя'
    )
    password = models.CharField(
        max_length=10,
        blank=True
    )

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER
