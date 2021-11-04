from django.db import models
from datetime import date
from users.models import User


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'date published', auto_now_add=True, blank=True
    )

    class Meta:
        ordering = ('-pub_date',)
