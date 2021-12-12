from fastapi import FastAPI
from src.config import app_config
from src.apps.auth.db.migration import migrate
from src.utils.controllers import ControllerLoader


app = FastAPI()
migrate()
controller_loader = ControllerLoader(base_dir=app_config.BASE_DIR, apps=["auth"])
controller_loader.detect(app)


