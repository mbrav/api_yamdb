#!/usr/bin/env python
# coding: utf-8


import os
import sys
import django
import csv
from django.contrib.auth import get_user_model


files = {
    'users': '../static/data/users.csv',
    'titles': '../static/data/titles.csv',
    'review': '../static/data/review.csv',
    'genre': '../static/data/genre.csv',
    'genre_title': '../static/data/genre_title.csv',
    'comments': '../static/data/comments.csv',
    'category': '../static/data/category.csv',
}


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
    User = get_user_model()
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
            print(f'Creating {new_user}')
            new_user.save()
        line_count += 1


def createTitles(csv_object):
    pass


def createReview(csv_object):
    pass


def createGenreTitle(csv_object):
    pass


def createComments(csv_object):
    pass


def createCategory(csv_object):
    pass


sys.path.append('..')
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
    django.setup()

    user_csv = import_from_csv(files['users'], output=True)
    titles_csv = import_from_csv(files['titles'], output=True)
    review_csv = import_from_csv(files['review'], output=True)
    genre_title_csv = import_from_csv(files['genre_title'], output=True)
    comments_csv = import_from_csv(files['comments'], output=True)
    category_csv = import_from_csv(files['category'], output=True)

    createUsers(csv_object=user_csv)
    createTitles(csv_object=user_csv)
    createReview(csv_object=user_csv)
    createGenreTitle(csv_object=user_csv)
    createComments(csv_object=user_csv)
    createCategory(csv_object=user_csv)
