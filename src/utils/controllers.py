import logging
import os


class Controllers:
    def __init__(self, base_dir: str, app_name: str):
        self.base_dir = os.path.join(base_dir, f"apps/{app_name}/controllers")
        self.app_name = app_name
        self.instances = {}

    def detect(self, app):
        files = [f for f in os.listdir(self.base_dir) if os.path.isfile(os.path.join(self.base_dir, f)) and f != "__init__.py"]
        for f in files:
            _controller_name = os.path.splitext(f)[0]
            _module = __import__(f"src.apps.{self.app_name}.controllers", fromlist=[_controller_name])

            try:
                logging.info(f"Loading {_module}, {_controller_name}")
                self.instances[_controller_name] = getattr(_module, _controller_name)
                app.include_router(getattr(_module, _controller_name).router)
            except Exception as e:
                logging.exception(f"Failed loading controller: {_controller_name} with exception: {str(e)}")
