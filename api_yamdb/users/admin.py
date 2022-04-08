from django.contrib import admin
from users.models import User
from reviews.models import (
    Categories, Genres, Title, Review, Comments
)


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        'confirmation_code',
    )
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class GenresAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category',)
    search_fields = ('name', 'description',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'score', 'pub_date', 'author',)
    search_fields = ('title', 'pub_date', 'author',)
    list_filter = ('title', 'pub_date', 'author',)
    empty_value_display = '-пусто-'


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('author', 'review', 'text', 'pub_date',)
    search_fields = ('review', 'pub_date', 'author',)
    list_filter = ('review', 'pub_date', 'author',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comments, CommentsAdmin)
