D:=docker
DEC:= exec -it
G:=git
DC:=docker-compose
D_DJANGO:=gbs-dj
D_POSTGRES:=gbs-psql

.PHONY:= build cleanfiles cleandjango run dj db dev clean deploy

build:
	${DC} build

cleanfiles:
	${G} clean -f gbs/migrations

cleandjango:
	${D} rm -f ${D_DJANGO} ${D_POSTGRES}
	${D} volume rm -f tine_pg_data tine_pg_backup

run:
	${DC} up -d

test:
	${D} ${DEC} ${D_DJANGO} python manage.py test gbs

dj:
	${D} ${DEC} ${D_DJANGO} python manage.py shell

ddump:
	${D} ${DEC} ${D_DJANGO} python manage.py dumpdata

pdump:
	${D} ${DEC} ${D_POSTGRES} su postgres -c 'pg_dump gbs'

db:
	${D} ${DEC} ${D_POSTGRES} su postgres -c 'psql'

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
