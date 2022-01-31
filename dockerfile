FROM python:3.9.7-slim-bullseye

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update --fix-missing
RUN apt-get install -y g++ libgdal-dev libpq-dev libgeos-dev libproj-dev openjdk-17-jre vim wait-for-it
RUN apt-get install -y curl git && pip install --upgrade pip

WORKDIR /code

RUN git clone https://github.com/opencdms/surface.git

RUN pip install numpy==1.21.2 --no-warn-script-location
RUN pip install -r surface/api/requirements.txt

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./src ./src
COPY ./scripts ./scripts
COPY entrypoint.sh ./entrypoint.sh
COPY init_climsoft_db.py ./init_climsoft_db.py
COPY mch.dbn ./mch.dbn
COPY MCHtablasycampos.def ./MCHtablasycampos.def

RUN useradd -m opencdms_api_user && chown -R opencdms_api_user /code

RUN ["chmod", "+x", "/code/scripts/load_initial_surface_data.sh"]

USER opencdms_api_user

ENTRYPOINT [ "/bin/sh", "entrypoint.sh" ]
