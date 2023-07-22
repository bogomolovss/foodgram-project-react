## Даннные для ревью
- Адрес сайта: bogomolovss.ru
- Email админ пользователя: admin@admin.ru
- Логин админ пользователя(используется для входа в админку): admin
- Пароль: admin

## Описание:
Foodgram is a site for finding new recipes and publishing your own. The service has the functionality of saving recipes to favorites and a shopping list, as well as subscriptions to other users.

# Как запустить проект
Copy docker-compose.production.yml on production server into directory foodgram.

Create .env file with info about PostgreSQL database.

Pull images from docker-hub
```
sudo docker compose -f docker-compose.production.yml pull
```

# Lauch all containers in docker compose
```
sudo docker compose -f docker-compose.production.yml up -d
```
# Migrate and collect static
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
```
```
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
```
## API examples:
### Create user:
```
 [POST]https://bogomolovss.ru/api/users/
{
  "username": "Name",
  "password": "123456789and"
  "email": "admin@admin.com",
}
```
### Answer:
```
{
    "email": "admin@admin.com",
    "username": "Name",
    "id": 1
}
```

### Get all recipes list:
```
    [GET]https://bogomolovss.ru/api/recipes/
```

