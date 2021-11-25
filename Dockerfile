FROM python:3.8-slim

RUN apt-get update -y \
    && apt-get install -y build-essential gcc git python3-dev g++ libffi-dev

RUN apt-get install -y libssl-dev libmariadb-dev libpq-dev
RUN apt-get install -y binutils libproj-dev gdal-bin

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY src /app/src

WORKDIR /app

ENTRYPOINT ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]

