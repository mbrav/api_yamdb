from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Comment
from users.models import User
from reviews.models import Comment, Title, Genres, Category, Review


class CommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    def validate(self, data):
        title = self.context.get('title')
        request = self.context.get('request')
        if (
            request.method != 'PATCH' and
            Review.objects.filter(title=title, author=request.user).exists()
        ):
            raise serializers.ValidationError('Оценка уже выставлена')
        return data

    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {'title': {'required': False}}
