import uvicorn
import os
from fastapi import FastAPI
from src.apps.climsoft.db.migration import migrate as migrate_climsoft_db
from src.apps.auth.db.migration import migrate as migrate_auth_db
from src.utils.controllers import Controllers

app = FastAPI()

BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))

# migrate
migrate_climsoft_db()
migrate_auth_db()

# load controllers
controllers = Controllers(base_dir=BASE_DIR, apps=["climsoft", "auth"])
controllers.detect(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
