FROM python:3.7

# set the argument default
ARG PORT=5000
ARG DATABASE_URL=postgres://postgres:postgres@postgres:5432/gbs

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
RUN python manage.py collectstatic

CMD python manage.py makemigrations && python manage.py migrate && python manage.py loaddata db && gunicorn tine.wsgi:application -w 2 -b :$PORT --reload --log-level DEBUG
