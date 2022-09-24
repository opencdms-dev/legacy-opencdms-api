FROM python:3.9.7-slim-bullseye

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update --fix-missing
RUN apt-get install -y g++ libgdal-dev libpq-dev libgeos-dev libproj-dev openjdk-17-jre vim wait-for-it r-base-core libmagick++-dev
RUN apt-get install -y curl git && pip install --upgrade pip Babel
RUN R -e "install.packages('magick')"

WORKDIR /code

RUN git clone https://github.com/opencdms/surface.git

RUN pip install numpy==1.21.2 --no-warn-script-location
RUN pip install -r surface/api/requirements.txt

COPY ./src ./src

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./scripts ./scripts
COPY entrypoint.sh ./entrypoint.sh
COPY mch.dbn ./mch.dbn
COPY MCHtablasycampos.def ./MCHtablasycampos.def
COPY climsoft-multi-deployment.yml ./climsoft-multi-deployment.yml

RUN ["chmod", "+x", "/code/scripts/load_initial_surface_data.sh"]

COPY ["pygeoapi-config.yml", "/code"]

ENTRYPOINT [ "/bin/sh", "entrypoint.sh" ]
