from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USER = 'user'
    MOD = 'moderator'
    ADMIN = 'admin'
    USER_ROLE_CHOICES = [
        (USER, 'Пользователь'),
        (MOD, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]

    bio = models.TextField(
        'Биография',
        blank=True,
    )

    role = models.CharField(
        max_length=9,
        choices=USER_ROLE_CHOICES,
        default=USER,
    )
