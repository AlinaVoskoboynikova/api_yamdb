from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from api.validators import validate_year
from reviews.models import Categories, Comments, Genres, Review, Title


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""
    class Meta:
        model = Categories
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров"""
    class Meta:
        model = Genres
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра произведений"""
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')
        read_only_fields = ('id',)

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score'))
        return rating.get('score__avg')


class TitleSerializerCreate(serializers.ModelSerializer):
    """Сериализатор для создания произведений"""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
        many=True
    )
    year = serializers.IntegerField(
        validators=[validate_year]
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )


class ReviewsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date',)
        read_only_fields = ('id', 'author', 'title')

    def create(self, validated_data):
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(title=title_id,
                                 author=self.context['request'].user).exists():
            raise serializers.ValidationError(
                'Нельзя оставить отзыв на одно и то же произведение дважды'
            )
        return Review.objects.create(**validated_data)


class CommentsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ('id', 'review')
