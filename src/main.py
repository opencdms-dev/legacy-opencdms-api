import uvicorn
from fastapi import FastAPI
from src.apps.climsoft.db.migration import migrate as migrate_climsoft_db
from src.apps.auth.db.migration import migrate as migrate_auth_db
from src.apps.surface.db.migration import migrate as migrate_surface_db
from src.utils.controllers import ControllerLoader
from src.config import app_config

app = FastAPI()


@app.on_event("startup")
async def run_migrations():
    # migrate
    migrate_climsoft_db()
    migrate_auth_db()
    await migrate_surface_db()
    # load controllers
    controller_loader = ControllerLoader(base_dir=app_config.BASE_DIR, apps=["climsoft", "auth", "surface"])
    controller_loader.detect(app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
