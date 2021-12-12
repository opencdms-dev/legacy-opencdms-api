# opencdms-server

OpenCDMS server uses Python FastAPI to expose a web interface for `opencdms-app` and other supported CDMSs.

### Application architecture

The application is designed to contain smaller child applications with separate set of configuration, i.e. separate database conenction.
Routes from this child applications will be combined in `src/main.py`

***Directory structure***

The root directory has two main directories:
- `src` : Contains all the applications/CDMS wrappers
- `tests` : Contains all the tests

Apart from these two directories we also have a docker-compose file contianing:

- `auth-db` service which is used for authentication
- `climsoft-db` service which should be used for storing Climsoft CDMS data
- `surface-db` service which should be used for storing Surface CDMS data
- `opencdms-server` is the application we are developing

There is also a `Dockerfile` where we have defined the docker image for `opencdms-server` service

*Project root*
```
.
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
├── src
│   ├── apps
│   ├── db
│   ├── main.py
│   └── utils
└── tests
    ├── app-name
    ├── ...other apps...
    ├── conftest.py
    └── datagen

```

In the app specific directory, the file structure is like below

*App root*

```
.
├── controllers
├── db
├── schemas
└── services

```

Controllers directory holds all the routes that we define. Routes are meant to handle application logic, i.e. authorization, data validation etc.

DB directory contains the DB configuration for respective app

Schemas directory contains all the DTOs defined as Pydantic Model

Services directory contains the business logic

### Running Development Server

The easiest way to go is running `docker-compose up -d --build`

The MCH database cannot be populated automatically. To populate the MCH database, do the following:

```bash
$ docker exec -it mchdb bash
$ mysql -u root -p mch < /scripts/create_mch_english_basic_tables.sql
```

Also, you can do the following:

```bash
$ pip3 install virtualenv 
$ virtualenv venv 
$ source venv/bin/activate
$ pip install -r requirements.txt
$ uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Note: You have to run database instance separately. Go to this repository for detail. https://github.com/opencdms/opencdms-test-data


### Running The Tests

Each master release should pass all the  To check if the tests are as expected or to add new feature or to fix some issue, you can run the tests on your own.

Follow these steps:

```bash
$ pip3 install virtualenv 
$ virtualenv venv 
$ source venv/bin/activate
$ pip install -r requirements.txt
$ docker-compose down -v
$ docker-compose up -d --build
$ pytest tests/integration
```

Additionally, you can run snapshot  We have collected a subset of data from production climsoft instance and we will run query on them to check if we are getting expected result.

  - From outside your project, run `git clone https://github.com/opencdms/opencdms-test-data`
  - `cd opencdms-test-data`
  - `docker-compose down -v`
  - `docker-compose up climsoft-4.1.1 --build`
  - Go to the project root `opencdms-server`
  - `source venv/bin/activate`
  - `export CLIMSOFT_DB_URI=mysql+mysqldb://root:password@127.0.0.1:33308/mariadb_climsoft_test_db_v4`
  - `pytest tests/snapshot`

