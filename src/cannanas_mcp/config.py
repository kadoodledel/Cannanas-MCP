from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    api_base_url: str
    api_key: str | None
    openapi_path: Path
    timeout_seconds: float
    transport: str


def get_default_openapi_path() -> Path:
    return Path(__file__).resolve().parents[2] / "cannanas-api-docs.yaml"


def load_settings() -> Settings:
    return Settings(
        api_base_url=os.getenv("CANNANAS_BASE_URL", "https://api.cannanas.club").rstrip("/"),
        api_key=os.getenv("CANNANAS_API_KEY"),
        openapi_path=Path(os.getenv("CANNANAS_OPENAPI_PATH", str(get_default_openapi_path()))),
        timeout_seconds=float(os.getenv("CANNANAS_TIMEOUT_SECONDS", "45")),
        transport=os.getenv("MCP_TRANSPORT", "stdio"),
    )
