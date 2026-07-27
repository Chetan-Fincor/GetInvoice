import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from app.config import NETWORK_SHARE_PATH


@dataclass(frozen=True)
class FolderCheckResult:
    client_code: str
    found: bool
    path: Path


def _is_safe_client_code(code: str) -> bool:
    if not code or code in {".", ".."}:
        return False
    return "/" not in code and "\\" not in code and ".." not in code


def parse_client_codes(raw_input: str) -> list[str]:
    """Split user input into unique, non-empty client codes."""
    if not raw_input or not raw_input.strip():
        return []

    parts = re.split(r"[\s,;]+", raw_input.strip())
    seen: set[str] = set()
    codes: list[str] = []

    for part in parts:
        code = part.strip()
        if code and code not in seen:
            seen.add(code)
            codes.append(code)

    return codes


def resolve_client_folder(
    client_code: str,
    base_path: Path | None = None,
) -> Path | None:
    if not _is_safe_client_code(client_code):
        return None

    root = base_path if base_path is not None else NETWORK_SHARE_PATH
    return root / client_code


def check_client_folders(
    client_codes: list[str],
    base_path: Path | None = None,
) -> list[FolderCheckResult]:
    results: list[FolderCheckResult] = []

    for code in client_codes:
        folder = resolve_client_folder(code, base_path)
        if folder is None:
            results.append(
                FolderCheckResult(
                    client_code=code,
                    found=False,
                    path=NETWORK_SHARE_PATH / code,
                )
            )
            continue

        results.append(
            FolderCheckResult(
                client_code=code,
                found=folder.is_dir(),
                path=folder,
            )
        )

    return results


def open_folder_in_explorer(folder_path: Path) -> bool:
    if not folder_path.is_dir():
        return False

    path_str = str(folder_path)

    if sys.platform == "win32":
        os.startfile(path_str)
        return True

    return False


def open_found_folders(results: list[FolderCheckResult]) -> list[str]:
    opened_codes: list[str] = []

    for result in results:
        if not result.found:
            continue
        if open_folder_in_explorer(result.path):
            opened_codes.append(result.client_code)

    return opened_codes
