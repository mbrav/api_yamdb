from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from datetime import date
from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Имя категории',
    )

    slug = models.SlugField(
        unique=True,
        verbose_name='Slug категории',
    )

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Имя жанра',
    )

    slug = models.SlugField(
        unique=True,
        verbose_name='Slug жанра',
    )

    def __str__(self):
        return self.name


class Title(models.Model):

    name = models.CharField(max_length=100)
    year = models.CharField(max_length=20)
    genre = models.ManyToManyField(
        Genres,
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='titles'
    )
    rating = models.FloatField(blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    author = models.ForeignKey(
        verbose_name='Автор отзыва',
        to=User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        verbose_name='Автор комментария',
        to=User,
        on_delete=models.CASCADE,
        related_name='Комментарии'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)
    review = models.ForeignKey(
        verbose_name='Обзор комментариев',
        to=Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Rating(models.Model):
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        help_text='Введите от 1 до 10',
        default=10,
        validators=[
            MinValueValidator(1, message='Оценка не может быть ниже 1.'),
            MaxValueValidator(10, message='Оценка не может быть больше 10.')
        ],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
