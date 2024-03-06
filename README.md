# Foodgram
Учебный проект Яндекс Практикум

![GitHub top language](https://img.shields.io/github/languages/top/hlystovea/foodgram-project-react)
![GitHub](https://img.shields.io/github/license/hlystovea/foodgram-project-react)
![GitHub Repo stars](https://img.shields.io/github/stars/hlystovea/foodgram-project-react)
![GitHub issues](https://img.shields.io/github/issues/hlystovea/foodgram-project-react)

## Описание
Проект о вкусной еде и рецептах. [Сайт](https://foodgram.hlystovea.ru) позволяет создавать рецепты, просматривать и добавлять в избранное рецепты других пользователей. Вы можете подписываться на авторов и добавлять рецепты в список покупок. 

## Технологии
- Python
- Django
- Django Rest Framework
- React
- Gunicorn
- Docker
- Nginx
- Postgres

## Установка (Linux)
У вас должен быть установлен [Docker Compose](https://docs.docker.com/compose/)

1. Клонирование репозитория 

```git clone https://github.com/hlystovea/foodgram-project-react.git```

2. Переход в директорию foodgram-project-react

```cd foodgram-project-react```

3. Создание файла с переменными окружения

```cp env.example .env```

4. Заполнение файла .env своими переменными

```nano .env```

5. Запуск проекта

```sudo docker compose up -d```

6. Запуск миграций

```sudo docker compose exec backend python manage.py migrate --noinput```

7. Сбор статических файлов

```sudo docker compose exec backend python manage.py collectstatic --no-input```

8. Создание суперпользователя

```sudo docker compose exec backend python manage.py createsuperuser```

9. Сайт будет доступен по адресу
 
```http://127.0.0.1:8002```

10. Админка сайта будет доступна по адресу

```http://127.0.0.1:8002/admin```

## Поддержка
Если у вас возникли сложности или вопросы по использованию проекта, создайте 
[обсуждение](https://github.com/hlystovea/foodgram-project-react/issues/new/choose) в данном репозитории или напишите в [Telegram](https://t.me/hlystovea).
