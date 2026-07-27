from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import APP_DESCRIPTION, APP_TITLE
from app.routes import home, invoice

APP_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")
app.include_router(home.router)
app.include_router(invoice.router)
