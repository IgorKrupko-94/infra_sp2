import datetime

from django.core.exceptions import ValidationError
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            title_id = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(author=user, title_id=title_id).exists():
                raise serializers.ValidationError('Ваш отзыв уже существует.')
        return data

    def validate_score(self, value):
        if (1 <= value <= 10) and int(value):
            return value
        raise serializers.ValidationError('Оценка - целое число от 1 до 10.')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise ValidationError(
                'Произведение не может иметь год позже текущего'
            )
        return value


class TitleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True)
    genre = GenreSerializer(many=True, required=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise ValidationError(
                'Произведение не может иметь год позже текущего'
            )
