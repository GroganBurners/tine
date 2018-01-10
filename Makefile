D:=docker
DC:=docker-compose

run:
	${DC} build
	${DC} up -d

clean:
	${DC} stop
	${DC} rm -f
	${D} volume rm -f tine_pg_data tine_pg_backup

