#!/bin/sh

python surface/api/manage.py migrate
./scripts/load_initial_surface_data.sh
exec $@
