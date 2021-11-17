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

    @property
    def is_admin(self):
        admin = self.is_staff or self.role == self.ADMIN
        return admin

    @property
    def is_mod(self):
        return self.role == self.MOD

    @property
    def is_usr(self):
        return self.role == self.USER

    @property
    def is_stf(self):
        staff = self.is_staff or self.role in [self.ADMIN, self.MOD]
        return staff

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
