import uvicorn
import os
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from src.apps.climsoft.controllers import station_controller, obselement_controller
from src.apps.climsoft.db.migration import migrate as migrate_climsoft_db
from src.db.engine import db_engine
from src.utils.controllers import Controllers

app = FastAPI()

app.add_middleware(DBSessionMiddleware, custom_engine=db_engine)

BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))

# migrate
migrate_climsoft_db(engine=db_engine)


controllers = Controllers(base_dir=BASE_DIR, app_name="climsoft")
controllers.detect(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
