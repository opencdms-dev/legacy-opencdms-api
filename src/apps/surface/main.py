from src.middlewares import auth
from fastapi import FastAPI
from src.config import app_config
from src.apps.surface.db.migration import migrate
from src.utils.controllers import ControllerLoader


app = FastAPI()
app.add_middleware(auth.AuthMiddleWare)


@app.on_event("startup")
async def run_migrations():
    await migrate()

    # load controllers
    controller_loader = ControllerLoader(base_dir=app_config.BASE_DIR, apps=["surface"])
    controller_loader.detect(app)
