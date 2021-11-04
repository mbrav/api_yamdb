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

    name = models.TextField()
    year = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='categories'
    )

    def __str__(self):
        return self.name


class Review(models.Model):

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        'Дата публикации ревью',
        auto_now_add=True,
        blank=True
    )


class Comment(models.Model):

    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации коммента',
        auto_now_add=True,
        blank=True
    )

    class Meta:
        ordering = ('-pub_date',)


class Rating(models.Model):
    text = models.TextField()
