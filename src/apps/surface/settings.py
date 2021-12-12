import django
from django.conf import settings
from src.config import app_config


def setup():
    try:
        settings.configure(
            DATABASES={
                "default": {
                    "ENGINE": "django.contrib.gis.db.backends.postgis",
                    "NAME": app_config.SURFACE_DB_NAME,
                    "USER": app_config.SURFACE_DB_USER,
                    "PASSWORD": app_config.SURFACE_DB_PASSWORD,
                    "HOST": app_config.SURFACE_DB_HOST,
                    "PORT": app_config.SURFACE_DB_PORT
                }
            },
            DEFAULT_AUTO_FIELD="django.db.models.AutoField",
            BASE_DIR=app_config.BASE_DIR,
            INSTALLED_APPS=(
                "src.apps.surface",
                "django.contrib.auth",
                "django.contrib.gis",
                "django.contrib.contenttypes"
            )
        )
    except RuntimeError:
        pass

    django.setup()
