#!/bin/sh
sleep 10
python /app/surface/api/manage.py migrate
python /app/surface/api/manage.py loaddata /app/surface/api/fixtures/*
uvicorn src.main:app --reload --host 0.0.0.0 --port 5000
exec $@
