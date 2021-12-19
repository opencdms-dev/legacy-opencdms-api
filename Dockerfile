FROM python:3.8-slim

RUN apt-get update -y --fix-missing\
    && apt-get install -y build-essential gcc git python3-dev g++ libffi-dev\
    && apt-get install -y g++ libgdal-dev libpq-dev libgeos-dev libproj-dev openjdk-17-jre vim wait-for-it\
    && apt-get --assume-yes install r-base-core


RUN apt-get install -y libssl-dev libmariadb-dev
RUN apt-get install -y binutils gdal-bin

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY src /app/src
COPY mch.dbn /app/mch.dbn
COPY MCHtablasycampos.def /app/MCHtablasycampos.def
COPY entrypoint.sh /app/entrypoint.sh

WORKDIR /app

#RUN git clone https://github.com/opencdms/surface-demo.git /app/surface
#RUN pip install -r /app/surface/api/requirements.txt

ENTRYPOINT ["/bin/sh", "/app/entrypoint.sh"]

