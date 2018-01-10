#!/bin/sh
git pull
git reset --hard origin/master
docker-compose build
docker-compose -f docker-compose-prod.yml up -d
