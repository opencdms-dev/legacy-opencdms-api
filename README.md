# opencdms-api

OpenCDMS server uses Python FastAPI to expose a web interface for `opencdms-app` and other supported CDMSs.

### Application architecture

The application is designed to contain smaller child applications with separate set of configuration, i.e. separate database conenction.
Routes from this child applications will be combined in `src/main.py`

***Directory structure***

The root directory has two main directories:
- `src` : Contains all the applications/CDMS wrappers
- `tests` : Contains all the tests

Apart from these two directories we also have three docker-compose files:

- `docker-compose.yml` For development
- `docker-compose.prod.yml` For production deployment (contains traefik config for https)
- `docker-compose.test.yml` For testing

These docker-compose files have all the necessary services to run `opencdms-api`

There is also a `dockerfile` where we have defined the docker image for `opencdms-api` service

*Project root*
```
.
├── create_mch_english_basic_tables.sql
├── docker-compose.prod.yml
├── docker-compose.test.yml
├── docker-compose.yml
├── dockerfile
├── entrypoint.sh
├── init_climsoft_db.py
├── makefile
├── mch.dbn
├── mch.dockerfile
├── MCHtablasycampos.def
├── poetry.lock
├── pyproject.toml
├── README.md
├── requirements-old.txt
├── requirements.txt
├── scripts
│   └── load_initial_surface_data.sh
├── src
│   └── opencdms_api
│       ├── config.py
│       ├── db.py
│       ├── deps.py
│       ├── __init__.py
│       ├── main.py
│       ├── middelware.py
│       ├── models.py
│       ├── router.py
│       ├── schema.py
│       └── templates
├── tests
│   ├── conftest.py
│   ├── __init__.py
│   └── test_router.py
└── traefik
    └── traefik.toml


```

### Running Development Server

The easiest way to go is running `docker-compose up -d --build`

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

To run the tests, you just need to run `docker-compose -f docker-compose.test.yml up --build`

Check the logs for error.

### How to access surface, climsoft, pygeoapi or mch API

OpenCDMS API server is a FastAPI application. surface, climsoft, pygeoapi, mch servers are
mounted to this FastAPI application. When mounting these child applications, we also have
enforced an Auth Middleware. So, if you want to access the endpoints on these child applications,
you have to make authenticated request.

To get an access token using default username and password:

```bash
$ curl -X 'POST' \
  'http://localhost:5070/auth' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "admin",
  "password": "password123"
}'
```

Say, it returns 

```bash
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY0MzgzMDUzMiwidG9rZW5fdHlwZSI6ImFjY2VzcyIsImp0aSI6ImEzM2Q4OWMyLTNlNmEtNDJlYS04MGZjLWViZjEzNTcyZjU5MSIsInVzZXJfaWQiOjF9.dp_wPSDZwL4HAN8JWCWyGRlL0s8gRvWKASUeDPQQygY"
}
```

Now you can make request to protected endpoints using this access token as `Bearer` token.

Here is an example:

```bash
$ curl -X 'GET' \
  'http://localhost:5070/climsoft/v1/acquisition-types/?limit=25&offset=0' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY0MzgzMDUzMiwidG9rZW5fdHlwZSI6ImFjY2VzcyIsImp0aSI6ImEzM2Q4OWMyLTNlNmEtNDJlYS04MGZjLWViZjEzNTcyZjU5MSIsInVzZXJfaWQiOjF9.dp_wPSDZwL4HAN8JWCWyGRlL0s8gRvWKASUeDPQQygY'
```

which will return something like this:

```bash
{"message":"Successfully fetched acquisition types.","status":"success","result":[]}
```

You can use Postman to make this requests easily.