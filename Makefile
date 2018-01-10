D:=docker
DEC:= exec -it
G:=git
DC:=docker-compose

run:
	${DC} build
	${DC} up -d

dj:
	${D} ${DEC} gbs-dj python manage.py shell

db:
	${D} ${DEC} gbs-psql su postgres -c 'psql'
clean:
	${DC} stop
	${DC} rm -f
	${D} volume rm -f tine_pg_data tine_pg_backup

deploy:
	${G} pull
	${G} reset --hard origin/master
	${DC} build
	${DC} -f docker-compose-prod.yml up -d
