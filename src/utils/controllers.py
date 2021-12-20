import logging
import os
from typing import List


class ControllerLoader:
    def __init__(self, base_dir: str, apps: List[str]):
        self.base_dirs = {
            app_name: os.path.join(base_dir, f"apps/{app_name}/controllers")
            for app_name in apps
        }
        self.instances = {}

    def detect(self, app):
        for app_name, base_dir in self.base_dirs.items():
            files = [f for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f)) and f != "__init__.py"]
            for f in files:
                _controller_name = os.path.splitext(f)[0]
                _module = __import__(f"apps.{app_name}.controllers", fromlist=[_controller_name])

                try:
                    logging.info(f"Loading {_module}, {_controller_name}")
                    self.instances[app_name+_controller_name] = getattr(_module, _controller_name)
                    app.include_router(getattr(_module, _controller_name).router)
                except Exception as e:
                    logging.exception(f"Failed loading controller: {_controller_name} with exception: {str(e)}")
