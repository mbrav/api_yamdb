from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Comment
from users.models import User
from reviews.models import Comment, Title, Genres, Category


class CommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class TitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(
        read_only=True, slug_field='category'
    )
    genres = SlugRelatedField(
        read_only=True, slug_field='genre'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__'
