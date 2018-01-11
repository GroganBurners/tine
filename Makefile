D:=docker
DEC:= exec -it
G:=git
DC:=docker-compose

.PHONY:= build cleanfiles cleandjango run dj db dev clean deploy 

build:
	${DC} build

cleanfiles:
	${G} clean -f gbs/migrations

cleandjango:
	${D} rm -f gbs-dj gbs-psql
	${D} volume rm -f tine_pg_data tine_pg_backup

run:
	${DC} up -d

dj:
	${D} ${DEC} gbs-dj python manage.py shell

db:
	${D} ${DEC} gbs-psql su postgres -c 'psql'

dev: cleanfiles build cleandjango run

clean: cleanfiles
	${DC} stop
	${DC} rm -f
	${D} volume rm -f tine_pg_data tine_pg_backup

deploy:
	${G} pull
	${G} reset --hard origin/master
	${DC} build
	${DC} -f docker-compose-prod.yml up -d
