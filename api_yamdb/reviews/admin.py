from django.contrib import admin

from .models import Category, Genres, Title, Review, Comment

# Register your models here.
admin.site.register(Category)
admin.site.register(Genres)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)
