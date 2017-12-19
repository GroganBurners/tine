FROM python:3.6-onbuild
RUN python manage.py collectstatic
