# opencdms-server

OpenCDMS server uses Python FastAPI to expose a web interface for `opencdms-app` and other applications

## Requirements

- Docker
- Docker compose
- Python 3.9
- Python virtualenvironment (I use `pyenv`)

## Dev

- create `.env`, `.surface_db.env` and `.mch_db.env` files
- Copy contents from `.example.env` to `.env`
- Copy contents from `.surface_db.example.env` to `.surface_db.env`
- Copy contents from `.mch_db.example.env` to `.mch_db.env`
- Activate virtual environment
- make install
- make surface_db_upgrade (To run the surface db migration)
- make surface_db_load_initial_data (To load the surface db with initial data)
- make serve (To start development server)
- visit `localhost:5070/docs` for swagger api documentation
- Surface api is mounted on path `localhost:5070/surface/*`
- Mch api is mounted on path `localhost:5070/mch/*`

`.surface_db.env` file sets the credentials for the surface postgres database
`.mch_db.env` file sets the credentials for the mch mysql database

### NOTE

In `docker-compose.yml` , `opencdms_api` service mounts the code directory into the container. Therefore the work directory
in the container will match your code structure. This means, if you don't have the `surface` project cloned, it would be removed
from the container once your volume is mounted.
For the surface api to work, with volume mounting, run `git clone https://github.com/Shaibujnr/surface.git surface`.
This will create a surface folder and clone the surface django project into it.

Alternatively: comment out the volume mounting (This will prevent reload on code change) and the cloned `surface` project
from the image would still be in the workdir.
