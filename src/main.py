import uvicorn
from fastapi import FastAPI
from src.apps.auth.main import app as auth_app
from src.apps.surface.main import app as surface_app
from src.apps.climsoft.main import app as climsoft_app


app = FastAPI()

app.mount("/auth", auth_app)
app.mount("/surface", surface_app)
app.mount("/climsoft", climsoft_app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
