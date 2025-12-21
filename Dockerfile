###########
# BUILDER #
###########

FROM python:3.11-slim-bookworm AS builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# lint
RUN pip install --upgrade pip
COPY . /usr/src/app/

# install python dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

FROM python:3.11-slim-bookworm

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/pomotracker
RUN mkdir $APP_HOME && mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

# migrate db changes ORM and collect static files
RUN rm -rf ${APP_HOME}/staticfiles/app && \
    cp -r ${APP_HOME}/app/static/* ${APP_HOME}/staticfiles/

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app
