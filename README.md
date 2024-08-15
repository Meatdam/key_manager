# Приложение "Key Manager" создание и отправка зашифрованных сообщений и паролей.
_____

Суть приложения:<br>
Пользователь создает сообщение, которое не хочет чтобы видели другие люди. Сообщение зашифровывается, и в зашифрованном виде хранится в БД. Расшифровать
может, только тот пользователь, который знает секретную фразу от сообщения. После того как пользователь создает сообщение, генерируется ссылка, на прочтение сообщения.
При попытке расшифровать сообщение, приложение ожидает ключевую фразу. Так же пользователь может задать время хранения сообщение, по дефолту сообщение храниться в БД 7 дней. 
Пользователь не может хранить свое зашифрованное сообщение больше 7 дней. Можно выбрать 1 день, 1 час или 7 дней по дефолту, если не задать время.
_____

Приложение выполнено на FastAPI framework<br>
## Стек:<br>
- FastApi;
- PostgreSQL;
- Celery;
- SQLAlchemy;
- Swagger;
- redoc;
- Alembic;
- psycopg2-binary;
- Dockefile;
- docker-compose;
- Redis.
_____
Данное приложение работает на взаимодействие API.<br>
Пользователь регестрируется, затем, необходимо получить токен, чтобы можно было создать секрет. После создания секрета, приходит зашифрованное сообщение, 
ключ и ссылка для расшифровке сообщения. Необходимо так же, не  забыть указать секретную фразу, при помощи которой можно было открыть сообщение.
____
### Важно:
При создании сообщения не забудьте указать секретную фразу.<br>
____
После создания сообщения пользователь может передать ссылку на сообщение, и другой  пользователь сможет прочитать данное сообщение, НО если введет секретное слово!<br>
_____
Для запуска проекта у себя локально без Docker необходимо:
1. git clone репозитория
```
git@github.com:Meatdam/key_manager.git
```
2. Установить виртуальное окружение `venv`
```
python3 -m venv venv для MacOS и Linux систем
python -m venv venv для windows
```
3. Активировать виртуальное окружение
```
source venv/bin/activate для MasOs и Linux систем
venv\Scripts\activate.bat для windows
```
4. установить файл с зависимостями
```
pip install -r requirements.txt
```
4. Создать базу данных в ```PgAdmin```, либо через терминал. Необходимо дать название в файле settings.py в каталоге 'base' в константе (словаре) 'DATABASES'
5. Заполнить своими данными файл .env в корне вашего проекта. Образец файла лежит в корне .env.example
6. Для запуска проекта использовать команду
```
uvicorn src.main:app --reload
```
иля запустить проект с файла `main.py`
7. Для запуска celery beat используйте команду
```
 celery -A src.celery_tasks beat -l INFO
```
8. Для запуска celery work используйте команду
```
celery -A src.celery_tasks worker -l INFO
```
Запуск приложения через Docker:<br>
1. Повторить шаги 1-3
2. Запустить Docker локально на машине
3. Выполнить команду в терминале
```
docker compose up -d --build
```
Данная команда сразу создаст образ, и сбилдит его, т.е. запустит локально в Docker<br>
4. Переходим по ссылке ```http://localhost:8000/```<br>
_____
Чтобы удалить контейнеры после работы с приложением используйте команду 
```
docker-compose down 
```
_____
Деплой приложения на удаленный сервер в ручном режиме.<br>
1. Необходимо установить зависимости на удаленный сервер
```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib python3-pip
apt install gunicorn
apt install nginx
```
2. Необходимо установить виртуальное окружение на удаленном сервере
```
python3 -m venv venv
```
3. Активировать виртуальное окружение
```
source venv/bin/activate
```
4. Скопировать свой проект на сервер
```
git clone <ssh вашего проекта с гит>
```
5. Установить все зависимости с файла requirements.txt
```
pip install -r requirements.txt
```
6. Настроить демон (gunicorn) на удаленном сервере yourproject.service и добавить данные в файл
```
[Unit]
Description=gunicorn daemon for Your Project # Описание вашего сервиса
After=network.target # Сервис, от которого будет зависеть запуск проекта

[Service]
User=yourusername # Имя пользователя владельца проекта в Linux
Group=yourgroupname # Группа, к которой относится пользователь
WorkingDirectory=/path/to/your/project # Путь к рабочей директории проекта
ExecStart=/path/to/venv/bin/gunicorn --config /path/to/gunicorn_config.py your_project.wsgi:application
# Команда для запуска проекта
```
7. Запустите сервис
```
sudo systemctl start yourproject
```
8. Настройка Nginx сервера для работы со статикой вашего проекта /etc/nginx/sites-available/my_site
```
server {
    listen 80;
    server_name <ip адрес или доменное имя сервера>;

    location /static/ {
			root /path/to/your/project/;
    }

    location /media/ {
			root /path/to/your/project/;
    }

    location / {
			include proxy_params;
			proxy_pass /path/to/your/project/project.sock
    }

}


```
9. Командой `nginx -t` проверяйте корретность заполнения файла
10. Подключите сайт к отображению
```
ln -s /etc/nginx/sites-available/my_site /etc/nginx/sites-enabled
```
11. Выполнить команду для определение статики проекта
```
python3 manage.py collectstatic
```
_____
Деплой приложения череез Docker на удаленный сервер
1. Выполнить шаги 1,3,5,6,7,8
2. Установить docker и docker-compose на удаленный сервер
```
apt install docker docker-compose
```
3. Выполнить команду
```
docker compose up -d --build
```
____
Подключение CI/CD
1. Регестрируемся на GitLab
2. Клонируем проект себе в GitLab используя SSH ключ
```
git@github.com:Meatdam/key_manager.git
```
3. В разделе settings -> CI/CD -> Runners создаем runner
4. В разделе settings -> CI/CD -> Variables создаем env файл для взаимодействия с проектом
5. Выполнить установку у себя на удаленном сервере
```
curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | sudo bash
sudo -E apt-get install gitlab-runner
```
____

Автор проекта:<br>
[Кузькин Илья](https://github.com/Meatdam)
