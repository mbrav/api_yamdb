from django.db.models.query import QuerySet
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from rest_framework.relations import SlugRelatedField

from reviews.models import Comment
from users.models import User
from reviews.models import Comment, Title, Genres, Category, Review


class CommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug')

class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=False)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        
class TitlepostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='slug')
    genre = serializers.SlugRelatedField(queryset=Genres.objects.all(), slug_field='slug', many=True)
    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        required=False,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        exclude = ('title',)
