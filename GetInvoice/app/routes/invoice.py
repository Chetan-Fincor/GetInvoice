from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.config import APP_DESCRIPTION, APP_TITLE
from app.services.folder_service import (
    FolderCheckResult,
    check_client_folders,
    open_found_folders,
    parse_client_codes,
)

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))


class SearchRequest(BaseModel):
    client_codes: list[str] = Field(min_length=1)


class SearchResultItem(BaseModel):
    client_code: str
    found: bool
    opened: bool = False


class SearchResponse(BaseModel):
    results: list[SearchResultItem]
    found_count: int
    not_found_count: int
    total_count: int
    opened_count: int


def _to_summary(results: list[FolderCheckResult]) -> dict[str, int]:
    found_count = sum(1 for result in results if result.found)
    return {
        "found_count": found_count,
        "not_found_count": len(results) - found_count,
        "total_count": len(results),
    }


def _serialize_results(
    results: list[FolderCheckResult],
    opened_codes: set[str],
) -> list[dict[str, object]]:
    return [
        {
            "client_code": result.client_code,
            "found": result.found,
            "opened": result.client_code in opened_codes,
        }
        for result in results
    ]


def _process_search(client_codes: str) -> tuple[list[FolderCheckResult], list[str], str | None]:
    codes = parse_client_codes(client_codes)
    if not codes:
        return [], [], "Enter at least one client code."

    results = check_client_folders(codes)
    opened_codes = open_found_folders(results)
    return results, opened_codes, None


@router.post("/search", response_class=HTMLResponse, name="search")
async def search_form(
    request: Request,
    client_codes: str = Form(default=""),
) -> HTMLResponse:
    results, opened_codes, error = _process_search(client_codes)
    summary = _to_summary(results) if results else None
    opened_set = set(opened_codes)

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "app_title": APP_TITLE,
            "app_description": APP_DESCRIPTION,
            "client_codes_input": client_codes,
            "results": _serialize_results(results, opened_set) if results else None,
            "summary": summary,
            "opened_codes": opened_codes,
            "error": error,
        },
    )


@router.post("/api/search", response_model=SearchResponse, name="search_api")
async def search_api(payload: SearchRequest) -> SearchResponse:
    codes = parse_client_codes(" ".join(payload.client_codes))
    if not codes:
        codes = [code.strip() for code in payload.client_codes if code.strip()]

    results = check_client_folders(codes)
    opened_codes = open_found_folders(results)
    opened_set = set(opened_codes)
    summary = _to_summary(results)

    return SearchResponse(
        results=[
            SearchResultItem(
                client_code=result.client_code,
                found=result.found,
                opened=result.client_code in opened_set,
            )
            for result in results
        ],
        opened_count=len(opened_codes),
        **summary,
    )
