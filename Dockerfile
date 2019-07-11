FROM python:3.7

# set the argument default
ARG DATABASE_URL=postgres://postgres:postgres@postgres:5432/gbs

RUN set -ex && pip install pipenv --upgrade
RUN set -ex && mkdir /usr/src/app

WORKDIR /usr/src/app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN set -ex && pipenv install --dev --deploy --system

COPY . /usr/src/app
RUN set -ex && python manage.py collectstatic

CMD python manage.py makemigrations && python manage.py migrate && python manage.py loaddata db && gunicorn tine.wsgi:application -w 2 -b :5000 --reload --log-level DEBUG
