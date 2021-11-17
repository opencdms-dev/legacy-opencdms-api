FROM python:3.8-alpine

RUN apk update \
    && apk add --no-cache postgresql-libs \
    && apk add --no-cache --virtual build-deps build-base gcc git python3-dev musl-dev postgresql-dev \
    && apk add --no-cache mariadb-dev

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

RUN apk --purge del build-deps

COPY src /app/src

WORKDIR /app

ENTRYPOINT ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]

