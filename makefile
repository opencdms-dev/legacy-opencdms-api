surface_db_upgrade:
	docker-compose run opencdms_api python surface/api/manage.py migrate

down:
	docker-compose down

serve:
	docker-compose up

served:
	docker-compose up -d

build:
	docker-compose build

bash:
	docker-compose run opencdms_api bash
