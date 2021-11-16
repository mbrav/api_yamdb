# Management commands readme

https://docs.djangoproject.com/en/3.2/howto/custom-management-commands/

Команды manage.py для api_yamdb

## Команда **csv_import**

Чтобы использовать:
`./manage.py csv_import`

Чтобы вывести информацию
Но не записывать в ДБ:
`./manage.py csv_import --run_only`

Указать имя таблицы:
`./manage.py csv_import --table users`

Помощь:
`./manage.py csv_import --help`
