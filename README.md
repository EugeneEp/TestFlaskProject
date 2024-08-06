# TestFlaskProject

### Введение:
**TestFlaskProject** - Небольшой Rest Api Token Based проект, написанный на Python, с использованием фреймворка Flask https://flask.palletsprojects.com/


### Архитектура проекта
При разработке архитектуры было использовано расширение **Flask-RESTX**:  
https://flask-restx.readthedocs.io/


### Реализованный функционал:

#### API:

### Auth

**[POST]**

*/api/v1/auth* - получить JWT токен **<API_TOKEN>**
JSON 
```
{
  `username`:"admin",
  `password`:"admin"
}
```

### Users
Headers
Authorization: **Bearer <API_TOKEN> (required)**

**[GET]**

*/api/v1/users?page=1&per_page=10* - получить всех пользователей с пагинацией
*/api/v1/users/{id}* - получить пользователя по id  

**[POST]**

*/api/v1/users* - создать пользователя  
JSON 
```
{
  `username`:"test123",
  `password`:"test123",
  `email`:"test123@mail.ru"
}
```

**[PATCH]**

*/api/v1/users/{id}* - обновить данные пользователя по id
JSON 
```
{
  `username`:"test321",
  `password`:"test321"
}
```
-----

### Docker Compose
sudo docker-compose up --build

> Для инициализации таблиц в бд используется flask-migrate  
> Файлы миграции появляются автоматически при выполнении сборки  
> По умолчанию порт бд 5432. Изменить ссылку на подключение можно через переменную окружения SQLALCHEMY_DATABASE_URI  
