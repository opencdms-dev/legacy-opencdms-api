from src.middlewares import auth
from fastapi import FastAPI
from src.config import app_config
from src.apps.climsoft.db.migration import migrate
from src.utils.controllers import ControllerLoader


app = FastAPI()
migrate()
app.add_middleware(auth.AuthMiddleWare)
controller_loader = ControllerLoader(base_dir=app_config.BASE_DIR, apps=["climsoft"])
controller_loader.detect(app)


