from middlewares import auth
from fastapi import FastAPI
from config import app_config
from apps.climsoft.db.migration import migrate
from utils.controllers import ControllerLoader


app = FastAPI()
migrate()
# app.add_middleware(auth.AuthMiddleWare)
controller_loader = ControllerLoader(base_dir=app_config.BASE_DIR, apps=["climsoft"])
controller_loader.detect(app)


