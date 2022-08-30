# Тестовое задание на вакансию Программист Python (Торговая сеть "Реми")

### Приложения проекта:
- main - основная папка - settings.py
- shop - описание моделей, views и т.п.
- core - фильтры и т.п.
- users - аутентификация пользователей

### Модели проекта:
- User - модель пользователей (AbstractUser)
- Category - модель категорий

### Ссылки проекта:
- index.html - главная страница

### Папки проекта:
- design - дизайн приложения - html, css
- main - главная папка проекта Django - setting.py
- media - хранение медиа-файлов (картинки товаров, категория)
- shop - приложение Django - магазин
- static - статика
- static_dev - статика для разработки

### Автор
Владимир Кириченко


### <span style="color:red"> В связи с тем, что данный проект является тестовым заданием - секретный ключ и другие возможные секретные данные не выносились в переменные окружения </span> 

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
Выполнить миграции:
```
python3 manage.py migrate
```
Для доступа в admin-панель создать суперюзера:
```
python3 manage.py createsuperuser
```
Запустить проект:
```
python3 manage.py runserver
```

