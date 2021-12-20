from fastapi import FastAPI
from config import app_config
from apps.auth.db.migration import migrate
from utils.controllers import ControllerLoader


app = FastAPI()
migrate()
controller_loader = ControllerLoader(base_dir=app_config.BASE_DIR, apps=["auth"])
controller_loader.detect(app)


