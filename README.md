# HorbykDmytroLABS

## Запуск локально

1. Клонуйте репозиторій і перейдіть в каталог через консоль:
git clone "repo_url"
cd "project_name"
2. Створіть віртуальне середовище та встановіть залежності:
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
3. Запустіть застосунок:
flask run --host=0.0.0.0 -p 5000
4. Перевірте роботу ендпоїнту
http://localhost:5000/healthcheck

## Запуск у Docker

1. Створіть Docker-образ:
docker build . -t myapp:latest
2. Запустіть контейнер:
docker run -it --rm -e PORT=5000 myapp:latest

## Запуск з Docker Compose
Зберіть і запустіть контейнер:
docker-compose build
docker-compose up