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

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать username.
        """
        return self.username

    def get_short_name(self):
        """ Аналогично с методом get_full_name(). """
        return self.username
