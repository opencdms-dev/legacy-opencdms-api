#!/bin/sh
python surface/api/manage.py migrate
./scripts/load_initial_surface_data.sh
pygeoapi openapi generate /code/pygeoapi-config.yml >| /code/pygeoapi-openapi.yml
uvicorn opencdms_api.main:app --host 0.0.0.0 --port 5000 --reload --use-colors
exec $@
