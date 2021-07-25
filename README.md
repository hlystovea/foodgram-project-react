# [foodgram](http://130.193.42.227/)

![workflow badge](https://github.com/hlystovea/foodgram-project-react/actions/workflows/main.yaml/badge.svg)

### Описание
Проект о вкусной еде и рецептах. Сайт позволяет создавать рецепты, просматривать рецепты других и добавлять их в избранное. Вы можете подписываться на авторов и добавлять рецепты в список покупок. 

### Технологии
- Python
- Django
- Django Rest Framework
- React
- Gunicorn
- Docker
- Nginx
- Postgres

### Запуск backend'а без Docker
1. Создать свой .env файл и сохранить его в корневом каталоге.
2. Установить pipenv.

```pip install pipenv```  

3. Запустить виртуальное окружение и установить зависимости.

```pipenv shell```
```pipenv install```

4. Запустить django.

```python manage.py runserver```
