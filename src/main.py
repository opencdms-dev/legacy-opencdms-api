import uvicorn
from fastapi import FastAPI
from src.apps.climsoft.db.migration import migrate as migrate_climsoft_db
from src.apps.auth.db.migration import migrate as migrate_auth_db
from src.apps.surface.db.migration import migrate as migrate_surface_db
from src.utils.controllers import ControllerLoader
from src.config import app_config
from src.apps.surface.settings import setup as setup_surface
from mch_api.api_mch import app as mch_api_application
from starlette.middleware.wsgi import WSGIMiddleware
from src.middlewares.auth import WSGIAuthMiddleWare


app = FastAPI()

app.mount("/mch", WSGIAuthMiddleWare(WSGIMiddleware(mch_api_application)))

# setup surface
setup_surface()
# migrate
migrate_climsoft_db()
migrate_auth_db()
# load controllers
controller_loader = ControllerLoader(base_dir=app_config.BASE_DIR, apps=["climsoft", "auth", "surface"])
controller_loader.detect(app)


@app.on_event("startup")
async def run_migrations():
    await migrate_surface_db()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
