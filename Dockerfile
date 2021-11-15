FROM python:3.8-alpine as base

# set environment variables
ENV TITAS=/home/app/titas
ENV APP_USER=titas_user

# set environment variables
ENV PYTHONFAULTHANDLER=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONHASHSEED=random
ENV PYTHONUNBUFFERED=1

RUN addgroup -S $APP_USER && adduser -S $APP_USER -G $APP_USER
# set work directory

RUN mkdir -p $TITAS
RUN mkdir -p $TITAS/static

# where the code lives
WORKDIR $TITAS

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.11

# install psycopg2 dependencies
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev jpeg-dev zlib-dev \
    && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev \
    && apk del build-deps \
    && apk --no-cache add musl-dev libffi-dev linux-headers g++

RUN pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION"

# copy project
COPY . $TITAS

# RUN pip install -r requirements.txt
RUN poetry install
COPY ./entrypoint.sh $TITAS

CMD ["/bin/bash", "/home/app/titas/entrypoint.sh"]