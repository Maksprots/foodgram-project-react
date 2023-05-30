 ## Продуктовый помощник - foodgram


---

 Приложение, которое позволит пользователям (авторизированным) постить рецепты, подписываться на авторов других рецептов,
 составлять списки необходимых продуктов и др, для неавторизованных же пользователей доступен просмотр рецептов.
 

 ***Для работы с проектом необходимо выполнить действия, описанные ниже.***
 ```bash
git clone <project>
cd foodgram-project-react/infra/
 ```
Создать файл .env и заполнить его данным
Пример
 ```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY ='8gmelpy0)8icp0##o(0#xy8#19p7ma6v4+pbnc)gsc3k64l!ce'
 ```
 

**Docker**
 ```bash
docker compose up -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --noinput
# Для заполнения базы тегами и ингредиентами нужно выполнить:
docker-compose exec backend python manage.py import_tags
docker-compose exec backend python manage.py import_ingredients
# Для заполнения базы пользователями и рецептами нужно выполнить:
docker-compose exec backend python manage.py data_test
```



***Технологии:***  
Python 3.9, Django 3.2, DRF 3.13, Nginx, Docker, Docker-compose, Postgresql, Github Actions.  

***Cервер:***
IP 158.160.28.249

***Админка:***
Login: admin
Password: admin777

***Тестовый пользователь:***
email: user1@yandex.ru
password: Qwerty999
