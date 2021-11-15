from django.db import models
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator

from django.db.models.aggregates import Min
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
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(
        Genres,
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='titles'
    )
    rating = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(
        verbose_name='review text',
    )
    author = models.ForeignKey(
        verbose_name='review author',
        to=User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    pub_date = models.DateTimeField(
        verbose_name='date of publication',
        auto_now_add=True)
    
    score = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        unique_together = ('title', 'author')

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField(
        verbose_name='comment text'
    )
    author = models.ForeignKey(
        verbose_name='comment author',
        to=User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='date of publication',
        auto_now_add=True)
    review = models.ForeignKey(
        verbose_name='comment to review',
        to=Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

