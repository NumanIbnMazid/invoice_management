# HELPER

* Install Redis on System

  * Debian
    $ sudo apt-get install redis-server
  * Arch
    $ sudo pacman -S redis

* Start Redis Server

  * Commands
    $sudo systemctl start redis
    $ sudo systemctl restart redis

* Docker Helper

* Buiding Docker Image

    $ docker build -t example_image .

* Run Docker Compose

    $ docker-compose up --build

  * For No Caching

    $ docker-compose build --no-cache

* Remove all images and containers

    $ docker-compose down --rmi all

* Check Docker Images

    $ docker images

* Tag a docker image

    $ docker tag example_image:latest numanibnmazid/example_repository:latest

* Pushing image to docker hub

    $ docker push numanibnmazid/example_repository:latest

* Project Runner Helper

* Ruuning Project with Uvicorn

    $ gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker

* Running Project Through Poetry

    $ poetry run python manage.py runserver
