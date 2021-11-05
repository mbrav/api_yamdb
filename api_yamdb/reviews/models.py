from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Review(models.Model):
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

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

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
