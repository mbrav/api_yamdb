import datetime as dt
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(
        read_only=True,
        many=False
    )
    genre = GenreSerializer(
        read_only=True,
        many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category')

    def validate_year(self, value):
        year = dt.datetime.today().year
        if value > year:
            raise serializers.ValidationError('Не правильно указан год')
        return value


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'pub_date', 'score', 'title')

    def validate_score(self, score):
        if score < 1 or score > 10:
            response = {
                'score': 'Должен быть между 1 и 10.'
            }
            raise serializers.ValidationError(response)
        return score

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        title = get_object_or_404(Title, id=title_id)
        if self.context['request'].method == 'POST':
            if Review.objects.filter(author=user, title=title).exists():
                response = {
                    'review': 'Уже есть такой отзыв.'
                }
                raise serializers.ValidationError(response)
        return data


class CommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    review = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    title = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
