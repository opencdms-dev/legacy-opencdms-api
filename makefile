surface_db_upgrade:
	docker-compose exec opencdms_api python surface/api/manage.py migrate

surface_db_load_initial_data:
	docker-compose exec opencdms_api bash scripts/load_initial_surface_data.sh

down:
	docker-compose down

serve:
	docker-compose up

served:
	docker-compose up -d

build:
	docker-compose build

bash:
	docker-compose exec opencdms_api bash

logs:
	docker-compose logs -f opencdms_api

install:
	pip install --upgrade pip poetry
	poetry install -v

test:
	docker-compose -f docker-compose.test.yml run test_opencdms_api; docker-compose -f docker-compose.test.yml down

make test-down:
	docker-compose -f docker-compose.test.yml down
