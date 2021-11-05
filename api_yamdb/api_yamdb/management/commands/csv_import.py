# Чтобы использовать:
# ./manage.py csv_import

import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genres, Rating, Review, Title

User = get_user_model()


def import_from_csv(csv_file, output=False):
    file = open(csv_file, 'r',)
    csv_reader = csv.reader(file, delimiter=',')
    line_count = 0
    if output:
        for row in csv_reader:
            if line_count == 0:
                print('\t'.join(row))
                line_count += 1
            else:
                output = ''
                for cell in row:
                    output += f'{cell} \t'
                print(output)
                line_count += 1
        print(f'Processed {line_count} lines.')
    return csv_reader


def createUsers(csv_object):
    line_count = 0
    for row in csv_object:
        if line_count > 0:
            new_user = User(
                id=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio='Test bio',
                first_name='First',
                last_name='Last',
            )
            print(f'Создаём User {new_user}')
            new_user.save()
        line_count += 1


def createCategory(csv_object):
    line_count = 0
    for row in csv_object:
        if line_count > 0:
            new_cat = Category(
                id=row[0],
                name=row[1],
                slug=row[2],
            )
            print(f'Создаём Category {new_cat}')
            new_cat.save()
        line_count += 1


def createTitles(csv_object):
    line_count = 0
    for row in csv_object:
        if line_count > 0:
            category = Category.objects.get(id=row[3])
            new_title = Title(
                id=row[0],
                name=row[1],
                year=row[2],
                category=category,
            )
            print(f'Создаём Title {new_title}')
            new_title.save()
        line_count += 1


def createReview(csv_object):
    line_count = 0
    for row in csv_object:
        if line_count > 0:
            pass


def createGenreTitle(csv_object):
    line_count = 0
    for row in csv_object:
        if line_count > 0:
            pass


def createComments(csv_object):
    line_count = 0
    for row in csv_object:
        if line_count > 0:
            pass


files = {
    'users': 'static/data/users.csv',
    'category': 'static/data/category.csv',
    'titles': 'static/data/titles.csv',
    'review': 'static/data/review.csv',
    'genre': 'static/data/genre.csv',
    'genre_title': 'static/data/genre_title.csv',
    'comments': 'static/data/comments.csv',
}


class Command(BaseCommand):

    help = "Загружает CSV фаилы заказчика в модели"

    def add_arguments(self, parser):
        parser.add_argument('-r', '--run_only', action='store_true',
                            help='Ничего не делать с базой, только пробежка', )

    def handle(self, *args, **kwargs):

        run_only = kwargs['run_only']

        self.stdout.write(self.style.MIGRATE_HEADING(
            'Имортируем данные заказчика'))

        user_csv = import_from_csv(files['users'], output=run_only)
        category_csv = import_from_csv(files['category'], output=run_only)
        titles_csv = import_from_csv(files['titles'], output=run_only)
        review_csv = import_from_csv(files['review'], output=run_only)
        genre_title_csv = import_from_csv(
            files['genre_title'], output=run_only)
        comments_csv = import_from_csv(files['comments'], output=run_only)

        if not run_only:
            self.stdout.write(self.style.WARNING('createUsers'))
            createUsers(csv_object=user_csv)
            self.stdout.write(self.style.WARNING('createCategory'))
            createCategory(csv_object=category_csv)
            # self.stdout.write(self.style.WARNING('createTitles'))
            # createTitles(csv_object=titles_csv)
            # self.stdout.write(self.style.WARNING('createReview'))
            # createReview(csv_object=review_csv)
            # self.stdout.write(self.style.WARNING('createGenreTitle'))
            # createGenreTitle(csv_object=genre_title_csv)
            # self.stdout.write(self.style.WARNING('createComments'))
            # createComments(csv_object=comments_csv)

        self.stdout.write(self.style.SUCCESS('Иморт Завершён!'))
