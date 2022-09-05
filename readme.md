# Тестовое задание на вакансию Программист Python (Торговая сеть "Реми")
## Работающий проект можно посмотреть - <http://45.141.103.185>

### Приложения проекта:
- api - приложения для взаимодействия посредством API
- main - основная папка - settings.py
- shop - описание моделей, views и т.п.
- core - фильтры и т.п.
- users - аутентификация пользователей, личный кабинет

### Модели проекта:
- User - модель пользователей (AbstractUser)
- Category - модель категорий
- Brand - бренды товаров
- Product - товары
- FavoriteProduct - вспомогательная модель для избранных товаров
- ImageProduct - изображения товаров
- ShoppingCartProduct - модель корзины пользователей 
- Order - заказы пользователей
- OrderProduct - модель для хранения товаров (с указанием количества) в заказах

### Ссылки проекта:
- index.html - главная страница
- category/<slug>/ - страница категории товаров 
- product/<id>/ - страница товара
- product/<id>/add_del_favorite/ - добавление/удаление товара из избранного для аутентифицированного пользователя
- product/<id>/add_product_in_shopping_cart/ - добавление товара в корзину
- product/<id>/increase_product_in_shopping_cart/ - увеличение товара в корзине на единицу
- product/<id>/reduce_product_in_shopping_cart/ - уменьшение товара в корзине на единицу
- product/<id>/delete_product_in_shopping_cart/ - удаление товара из корзины
- product/search_product/ - поиск товаров
- auth/ - аутентификация пользователей
- auth/cabinet/ - личный кабинет пользователя
- auth/cabinet/favorite_product/ - избранные товары пользоватля 
- auth/cabinet/shopping_cart/ - корзина пользователя 
- auth/cabinet/shopping_cart/clean_shopping_cart/ - очистка корзины
- auth/cabinet/ordering/ - оформление заказа
- auth/cabinet/order_detail/<id>/ - детали заказа
- auth/cabinet/order_list/ - все заказы пользователя

### Эндпоинты API:
#### Users:
- api/auth/users/ - GET, POST(регистрация пользователя)
- api/auth/users/{id} - GET, PATCH, DELETE
- api/auth/token/login/ - POST - полуение токена
- api/auth/token/logout/ - POST - удаление токена
- api/auth/users/me/ - GET
- api/auth/set_password/ - POST
#### Products:
- api/products/ - GET
- api/products/{id} - GET
- api/products/?category=slug - GET - фильтр товаров по категории (slug-категории) (чтобы отразился товар, он должен принадлежать именно этой категории, но не дочерним)
- api/products/?is_favorited=1 - GET - выводит все избранные товары избранные аутентифицированным пользователем 
- api/products/?is_in_shopping_cart=1 - GET - выводит все товары, находящиеся в корзине у аутентифицированного пользователя
- api/products/?search=запрос - GET - выводит товары по поиску (поиск осуществляется по имени товара и по имени конечной категории) (запрос на кириллице при работе с БД SQLite осуществляется только с учетом регистра)
- api/products/<id>/favorite - POST, DELETE - помещение товара в избранное, удаление товара из избранного для аутентифицированного пользователя
- api/products/<id>/shopping_cart - POST, DELETE - помещение товара в корзину, удаление товара из корзины для аутентифицированного пользователя
- api/products/<id>/shopping_cart/increase - POST - увеличение товара на одну единицу, назодящегося в корзине у аутентифицированного пользователя
- api/products/<id>/shopping_cart/reduce - POST - уменьшение товара на одну единицу, назодящегося в корзине у аутентифицированного пользователя

### Папки проекта:
- api - приложение Django - API
- core - приложение Django - фильтры
- design - дизайн приложения - html, css
- main - главная папка проекта Django - setting.py
- media - хранение медиа-файлов (картинки товаров, категория)
- sent_emails - для отладочной отправки почты пользователям
- shop - приложение Django - магазин
- static - статика
- static_dev - статика для разработки
- templates - шаблоны HTML
- users - приложение Django - аутентификация пользователей

### Автор
Владимир Кириченко


### <span style="color:red"> В связи с тем, что данный проект является тестовым заданием, для удобства проверки работоспособности - база данных, статичные файлы, медиа файлы, файл с переменными окружения также коммитятся. </span> 

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/.../
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
. env/bin/activate (для linux)
sourse env/Scripts/activate (для Windows)
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
### <span style="color:red"> База данных также комитится, поэтому миграцию и суперюзера делать нет необходимости </span>
### <span style="color:red"> Суперюзер - admin, пароль - 12345 </span>

Запустить проект:
```
python3 manage.py runserver
```

