import uvicorn
import os
from fastapi import FastAPI
from sqlalchemy import create_engine
from fastapi_sqlalchemy import DBSessionMiddleware
from apps.climsoft.controllers import station_controller
from apps.climsoft import db as climsoft_db

app = FastAPI()

db_url = os.getenv("DATABASE_URI", "mysql+mysqldb://root:password@127.0.0.1:33308/climsoft_dev")
db_engine = create_engine(db_url)

app.add_middleware(DBSessionMiddleware, custom_engine=db_engine)

# migrate
climsoft_db.migrate(engine=db_engine)


app.include_router(station_controller.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
