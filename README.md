## Проект api_yamdb

#### Технологии

-   Python 3.7
-   Django 2.2
-   DjangoRestFramework 3.12

## Установка

Для локальной установки прежде всего нужно убедится, что установлен Python с версией >3.7. Далее следует:

-   Клонировать репозиторий:

```
git clone https://github.com/kudinov-prog/api_yamdb_kudinov.git
```

-   Установить и активировать виртуальное окружение:

```
cd api_yamdb/api_yamdb

python -m venv venv

source venv/bin/activate
```

-   Установить зависимости pip:

```
pip install -r requirements.txt
```

-   Создать миграции:

```
python manage.py makemigrations

python manage.py migrate
```

-   Загрузить тестовые данные:

```
python manage.py csv_import

```

-   Запустить сервер:

```
python manage.py runserver
```

-   Эндпойнты будут доступны по адресу: [http://127.0.0.1:8000/api/v1/](http://127.0.0.1:8000/api/v1/)
