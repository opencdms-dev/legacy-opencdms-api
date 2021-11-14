import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from src.apps.climsoft.controllers import station_controller
from src.apps.climsoft.db.migration import migrate as migrate_climsoft_db
from src.db.engine import db_engine

app = FastAPI()

app.add_middleware(DBSessionMiddleware, custom_engine=db_engine)

# migrate
migrate_climsoft_db(engine=db_engine)


app.include_router(station_controller.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
