[![Continous Integration](https://github.com/GroganBurners/tine/workflows/Continous%20Integration/badge.svg)](https://github.com/GroganBurners/tine/actions?query=workflow%3A%22Continous+Integration%22) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Coverage Status](https://coveralls.io/repos/github/GroganBurners/tine/badge.svg?branch=master)](https://coveralls.io/github/GroganBurners/tine?branch=master) [![Test Coverage](https://api.codeclimate.com/v1/badges/a717383eb45c93857570/test_coverage)](https://codeclimate.com/github/GroganBurners/tine/test_coverage) [![Maintainability](https://api.codeclimate.com/v1/badges/a717383eb45c93857570/maintainability)](https://codeclimate.com/github/GroganBurners/tine/maintainability)

# tine
A Django web application for Grogan Burner Services, a heating systems installation, repair and service company.


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
