from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Имя категории',
    )

    slug = models.SlugField(
        unique=True,
        verbose_name='Slug категории',
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Имя жанра',
    )

    slug = models.SlugField(
        unique=True,
        verbose_name='Slug жанра',
    )

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Title(models.Model):

    name = models.CharField(max_length=100)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='titles'
    )

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'

    @property
    def rating(self):
        reviews = self.reviews.all()
        score_avg = reviews.aggregate(models.Avg('score')).get('score__avg')
        return None if isinstance(score_avg, type(None)) else int(score_avg)

    def __str__(self):
        return self.name


class Review(models.Model):

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    text = models.TextField(
        verbose_name='Review text',
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Review author',
        related_name='reviews',
        db_column='author'
    )

    pub_date = models.DateTimeField(
        verbose_name='date of publication',
        auto_now_add=True,
        db_index=True
    )

    score = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(0),
                    MaxValueValidator(10)]
    )

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ('-pub_date',)
        unique_together = ('title', 'author')

    def __str__(self):
        return f'{self.title}, {self.pub_date}, {self.score}/10'


class Comment(models.Model):
    text = models.TextField(
        verbose_name='comment text'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='comment author',
        on_delete=models.CASCADE,
        related_name='comments'
    )

    pub_date = models.DateTimeField(
        verbose_name='date of publication',
        auto_now_add=True
    )

    review = models.ForeignKey(
        verbose_name='comment to review',
        to=Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'{self.author}, {self.pub_date}, "{self.text[:30]}"'
