[![Continous Integration](https://github.com/GroganBurners/tine/workflows/Continous%20Integration/badge.svg)](https://github.com/GroganBurners/tine/actions?query=workflow%3A%22Continous+Integration%22) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Coverage Status](https://coveralls.io/repos/github/GroganBurners/tine/badge.svg?branch=master)](https://coveralls.io/github/GroganBurners/tine?branch=master) [![Test Coverage](https://api.codeclimate.com/v1/badges/a717383eb45c93857570/test_coverage)](https://codeclimate.com/github/GroganBurners/tine/test_coverage) [![Maintainability](https://api.codeclimate.com/v1/badges/a717383eb45c93857570/maintainability)](https://codeclimate.com/github/GroganBurners/tine/maintainability)

# tine
A Django web application for Grogan Burner Services, a heating systems installation, repair and service company.

## Seasonal homepage banners

In Django admin, open **Hero images** and create a banner for each season. Set
the image, title, teaser text (the message), optional button, and **Season**, then
enable **Active**. The homepage automatically selects the matching banner on each
request, using the date in `Europe/Dublin`:

| Season | Months |
| --- | --- |
| Spring | March–May |
| Summer | June–August |
| Autumn | September–November |
| Winter | December–February |

These are [Met Éireann's meteorological seasons](https://www.met.ie/climate/climate-of-ireland).
Keep an active **All year** banner as a fallback when no active seasonal banner
matches. Existing banners default to **All year**. If multiple active banners
match, the oldest is used; if none match and there is no fallback, the banner
section is hidden. Images and messages switch together at Irish midnight on the
first day of each season. No Celery worker or scheduled job is needed.

Run `python manage.py migrate` before starting the updated app to add the season
field. Python 3.14 and the dependencies in `requirements.txt` are required.

## Tests and coverage

With `DATABASE_URL` pointing to a PostgreSQL database, run:

```sh
coverage run manage.py test gbs
coverage report
coverage html
```

CI requires at least **90% application statement coverage**. Coverage includes
the `gbs` application and management commands, excluding generated migrations
and test code. Browser tests are optional and are not enabled in normal CI runs.

The upgraded Django also requires a supported PostgreSQL server. The legacy
PostgreSQL 10.4 image in `docker-compose.yml` needs a database upgrade before
running the updated application locally. Preserve and migrate existing data;
do not point a newer PostgreSQL image at the old data directory.


[![Sauce Test Status](https://saucelabs.com/browser-matrix/groganburners.svg)](https://saucelabs.com/u/groganburners)

# Deployment
## Local Deployment
1. use `docker-compose build && docker-compose up -d` to build and bring up Django/Postgres containers.
2. Open `http://localhost:5000`

## Server Deployment
### On Server:
1. Get Dokku Install script: `wget https://raw.githubusercontent.com/dokku/dokku/v0.19.11/bootstrap.sh`
2. Run Dokku Install script: `sudo DOKKU_TAG=v0.19.11 bash bootstrap.sh`
3. Create Dokku app: `sudo dokku apps:create tine`
4. Install Postgres Dokku plugin: `sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git`
5. Create Database: `sudo dokku postgres:create gbs`
6. Link Database to app: `dokku postgres:link gbs tine`

### On local machine:
1. Add `git remote add dokku dokku@dokku.me:tine`
2. Push `git push dokku master`

### License
This project is MIT licensed for all the source code. Images and Artwork are full copyright of their owners.
