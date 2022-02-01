#!/bin/sh

python surface/api/manage.py migrate
python init_climsoft_db.py
./scripts/load_initial_surface_data.sh
pygeoapi openapi generate /code/pygeoapi-config.yml >| /code/pygeoapi-openapi.yml
exec $@
