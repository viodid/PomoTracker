# # Use an official Python image as the base
# FROM python:3.11-bullseye

# # Set environment variables for Python
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Create and set the working directory
# WORKDIR /app

# # Copy and install Python dependencies
# COPY requirements.txt /app/
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the application code
# COPY . /app/

# # Collect static files and set the owner to www-data
# RUN python manage.py collectstatic --noinput

# # Migrate the database
# RUN python manage.py migrate

# # Install NGINX
# RUN apt-get update && apt-get install -y nginx

# # Copy the custom NGINX configuration
# COPY config/nginx/nginx.conf /etc/nginx/conf.d/default.conf

# # Create the Nginx log folder
# RUN mkdir -p /var/log/nginx/pomotracker && \
#     touch /var/log/nginx/pomotracker/access.log && \
#     touch /var/log/nginx/pomotracker/error.log && \
#     chown -R www-data /var/log/nginx/pomotracker && \
#     chown -R www-data /var/lib/nginx && \
#     chown -R www-data /var/www/pomotracker && \
#     chown www-data /etc/nginx/conf.d/default.conf

# # Start Gunicorn and NGINX in the foreground
# CMD gunicorn PomoTracker.wsgi:application --bind 0.0.0.0:8000




###########
# BUILDER #
###########

# pull official base image
FROM python:3.11.4-slim-buster as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# lint
RUN pip install --upgrade pip
#RUN pip install flake8==6.0.0
COPY . /usr/src/app/
#RUN flake8 --ignore=E501,F401 .

# install python dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.11.4-slim-buster

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

# Migrate the database
RUN python manage.py migrate

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app