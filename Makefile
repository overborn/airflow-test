build:
	docker-compose build
init:
	docker-compose up airflow-init
up:
	docker-compose up
up-all: # not working now
	COMPOSE_PROFILES=fastapi,generator docker-compose up
down:
	docker-compose down --volumes
cleanup:
	docker-compose down --volumes --rmi all