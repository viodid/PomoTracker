FROM python:3.11

# Path: /app
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN apt update && apt install -y nginx

RUN python manage.py collectstatic

RUN gunicorn -c config/gunicorn/prod.py

