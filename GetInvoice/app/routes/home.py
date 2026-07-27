from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import APP_DESCRIPTION, APP_TITLE

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))


@router.get("/", response_class=HTMLResponse, name="home")
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "app_title": APP_TITLE,
            "app_description": APP_DESCRIPTION,
            "client_codes_input": "",
            "results": None,
            "summary": None,
            "opened_codes": [],
            "error": None,
        },
    )
