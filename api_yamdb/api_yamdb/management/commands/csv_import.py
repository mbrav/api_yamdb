# Чтобы использовать:
# ./manage.py csv_import
#
# Чтобы вывести информацию
# Но не записывать в ДБ
# ./manage.py csv_import --run_only
#
# Указать имя таблицы
# ./manage.py csv_import --table users
#
# Помощь
# ./manage.py csv_import --help

from pathlib import Path
import os
import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genres, Rating, Review, Title

# Find the project base directory
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.abspath(__file__)
# Specify number of directories to go up from current file
PATH_UP = 3
BASE_DIR = str(Path(FILE_PATH).parents[PATH_UP])


User = get_user_model()


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


def createGenre(csv_object):
    line_count = 0
    for row in csv_object:
        if line_count > 0:
            new_genre = Genres(
                id=row[0],
                name=row[1],
                slug=row[2],
            )
            print(f'Создаём Genres {new_genre}')
            new_genre.save()
        line_count += 1


def createGenreTitle(csv_object):
    line_count = 0
    for row in csv_object:
        if line_count > 0:
            genre = Genres.objects.get(id=row[2])
            title = Title.objects.get(id=row[1])
            genre.titles.add(title)
            genre.save()
            print(f'Создаём связь между Title {title} и Genre {genre}')
        line_count += 1


def createComments(csv_object):
    line_count = 0
    for row in csv_object:
        if line_count > 0:
            pass


def createReview(csv_object):
    line_count = 0
    for row in csv_object:
        if line_count > 0:
            title = Title.objects.get(id=row[1])
            author = User.objects.get(id=row[3])
            new_review = Review(
                id=row[0],
                title=title,
                text=row[2],
                author=author,
                score=row[4],
                pub_date=row[5],
            )
            print(f'Создаём Review {new_review}')
            new_review.save()
        line_count += 1


files = {
    'users': f'{BASE_DIR}/static/data/users.csv',
    'category': f'{BASE_DIR}/static/data/category.csv',
    'titles': f'{BASE_DIR}/static/data/titles.csv',
    'genre': f'{BASE_DIR}/static/data/genre.csv',
    'genre_title': f'{BASE_DIR}/static/data/genre_title.csv',
    'comments': f'{BASE_DIR}/static/data/comments.csv',
    'review': f'{BASE_DIR}/static/data/review.csv',
}


class Command(BaseCommand):

    help = """Загружает CSV фаилы заказчика в модели"""

    def import_from_csv(self, csv_file, output=False):

        file = open(csv_file, 'r',)
        csv_reader = csv.reader(file, delimiter=',')
        line_count = 0
        if output:
            self.stdout.write(self.style.MIGRATE_HEADING(
                f'\nТаблицы в фаиле "{csv_file}".'))
            for row in csv_reader:
                if line_count == 0:
                    self.stdout.write(self.style.SQL_FIELD('\t'.join(row)))
                    line_count += 1
                else:
                    out = ''
                    for cell in row:
                        out += f'{cell} \t'
                        self.stdout.write(self.style.SQL_TABLE(out))
                    line_count += 1
            self.stdout.write(self.style.SQL_KEYWORD(
                f'Всего {line_count} записей.\n'))
        return csv_reader

    def add_arguments(self, parser):
        parser.add_argument('-r', '--run_only', action='store_true',
                            help='Ничего не делать с базой, только пробежка.', )
        parser.add_argument('-t', '--table', type=str,
                            help=f'Указать таблицу название таблицы. Доступны: {", ".join(files.keys())}.')

    def handle(self, *args, **kwargs):

        run_only = kwargs['run_only'] == True
        table = kwargs['table']

        self.stdout.write(self.style.MIGRATE_HEADING(
            'Имортируем данные заказчика'))

        if table:
            specified_csv = self.import_from_csv(files[table], output=run_only)
            self.stdout.write(self.style.WARNING(files[table]))
            createUsers(csv_object=specified_csv)
        else:
            user_csv = self.import_from_csv(files['users'], output=run_only)
            category_csv = self.import_from_csv(
                files['category'], output=run_only)
            titles_csv = self.import_from_csv(files['titles'], output=run_only)
            genre_csv = self.import_from_csv(
                files['genre'], output=run_only)
            genre_title_csv = self.import_from_csv(
                files['genre_title'], output=run_only)
            comments_csv = self.import_from_csv(
                files['comments'], output=run_only)
            review_csv = self.import_from_csv(files['review'], output=run_only)

            if not run_only:
                self.stdout.write(self.style.WARNING('createUsers'))
                createUsers(csv_object=user_csv)
                self.stdout.write(self.style.WARNING('createCategory'))
                createCategory(csv_object=category_csv)
                self.stdout.write(self.style.WARNING('createTitles'))
                createTitles(csv_object=titles_csv)
                self.stdout.write(self.style.WARNING('createGenre'))
                createGenre(csv_object=genre_csv)
                self.stdout.write(self.style.WARNING('createGenreTitle'))
                createGenreTitle(csv_object=genre_title_csv)
                # self.stdout.write(self.style.WARNING('createComments'))
                # createComments(csv_object=comments_csv)
                # self.stdout.write(self.style.WARNING('createReview'))
                # createReview(csv_object=review_csv)

        self.stdout.write(self.style.SUCCESS('Иморт Завершён!'))
