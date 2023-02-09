from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title
from users.models import User


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author', 'text', 'score', 'pub_date',)
    search_fields = ('title', 'author', 'score', 'pub_date',)
    list_filter = ('pub_date', 'score')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'text', 'author', 'pub_date',)
    search_fields = ('review', 'author', 'pub_date',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name',
                    'bio', 'role', 'confirmation_code',)
    search_fields = ('username', 'role',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category', 'description',)
    search_fields = ('name', 'year',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
