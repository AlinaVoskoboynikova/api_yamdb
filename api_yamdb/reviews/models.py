from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.constraints import UniqueConstraint

from api.validators import validate_year

User = get_user_model()


class Categories(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Категория',
        help_text='Укажите категорию'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='Уникальный идентификатор',
        help_text='Укажите уникальный идентификатор категории'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Жанр',
        help_text='Укажите жанр'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='Уникальный идентификатор',
        help_text='Укажите уникальный идентификатор жанра'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Произведение',
        help_text='Укажите произведение'
    )
    year = models.IntegerField(
        validators=(validate_year,),
        verbose_name='Год создания',
        help_text='Укажите год создания произведения'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        max_length=200,
        blank=True,
        null=True,
        related_name='titles',
        help_text='Укажите категорию',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genres,
        related_name='titles',
        help_text='Укажите жанр',
        verbose_name='Жанр'
    )

    class Meta:
        ordering = ('year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        help_text='Укажите произведение',
        verbose_name='Произведение'
    )
    text = models.TextField(
        help_text='Введите текст',
        verbose_name='Текст'
    )
    score = models.PositiveSmallIntegerField(
        help_text='Введите оценку от 1 до 10',
        verbose_name='Оценка')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
        help_text='Автор',
        verbose_name='Автор'
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=['title', 'author'], name='unique_following'
            ),
        )
        ordering = ('pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.title


class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
        help_text='Автор',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        help_text='Отзыв',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        help_text='Введите текст',
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.review
