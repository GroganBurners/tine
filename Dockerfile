FROM python:3.6.3

RUN set -ex && pip install pipenv --upgrade
RUN set -ex && mkdir /usr/src/app

WORKDIR /usr/src/app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN set -ex && pipenv install --dev --deploy --system

COPY . /usr/src/app
RUN set -ex && python manage.py collectstatic

CMD python manage.py makemigrations && python manage.py migrate && python manage.py loaddata db && gunicorn tine.wsgi:application -w 2 -b :8000 --reload --log-level DEBUG
