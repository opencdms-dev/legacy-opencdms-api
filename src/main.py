import uvicorn
from fastapi import FastAPI
from apps.climsoft.db.migration import migrate as migrate_climsoft_db
from apps.auth.db.migration import migrate as migrate_auth_db
# from apps.surface.db.migration import migrate as migrate_surface_db
from utils.controllers import ControllerLoader
from config import app_config
# from apps.surface.settings import setup as setup_surface
from mch_api.api_mch import app as mch_api_application
from starlette.middleware.wsgi import WSGIMiddleware
from middlewares.auth import WSGIAuthMiddleWare


app = FastAPI()

app.mount("/mch", WSGIAuthMiddleWare(WSGIMiddleware(mch_api_application)))
# app.mount("/surface", WSGIAuthMiddleWare(WSGIMiddleware(
# surface_application)))


# setup surface
# setup_surface()
# migrate
migrate_climsoft_db()
migrate_auth_db()
# load controllers
controller_loader = ControllerLoader(
    base_dir=app_config.BASE_DIR,
    apps=["climsoft", "auth"]
)
controller_loader.detect(app)

# @app.on_event("startup")
# async def run_migrations():
#     await migrate_surface_db()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
