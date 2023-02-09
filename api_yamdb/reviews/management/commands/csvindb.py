import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

CSV_FILES = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    GenreTitle: 'genre_title.csv'
}


class Command(BaseCommand):

    def handle(self, *args, **options):
        for model, file in CSV_FILES.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{file}',
                encoding='utf-8'
            ) as csvfile:
                for row in csv.DictReader(csvfile):
                    model.objects.get_or_create(**dict(row))
