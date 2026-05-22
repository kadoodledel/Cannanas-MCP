from __future__ import annotations

import base64
import json
from typing import Any
from urllib.parse import urlencode

import httpx

from cannanas_mcp.openapi_index import OperationSpec


class CannanasClient:
    LIST_CONTAINER_KEYS = ("data", "items", "results", "records", "rows", "clubs", "locations", "members")

    def __init__(self, *, base_url: str, api_key: str, timeout_seconds: float) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds

    async def call_operation(
        self,
        *,
        operation: OperationSpec,
        rendered_path: str,
        query_params: dict[str, Any] | None = None,
        body: Any = None,
    ) -> dict[str, Any]:
        url = f"{self.base_url}{rendered_path}"
        if query_params:
            url = f"{url}?{urlencode(self._flatten_query_params(query_params), doseq=True)}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
        request_kwargs: dict[str, Any] = {"headers": headers}
        body_request_kwargs = self._build_body_request_kwargs(operation, body)
        extra_headers = body_request_kwargs.pop("headers", None)
        if extra_headers:
            request_kwargs["headers"].update(extra_headers)
        request_kwargs.update(body_request_kwargs)

        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.request(operation.method, url, **request_kwargs)

        result: dict[str, Any] = {
            "ok": response.is_success,
            "status_code": response.status_code,
            "method": operation.method,
            "url": url,
        }
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            result["data"] = response.json()
        else:
            result["data"] = response.text
        if not response.is_success:
            result["error"] = "Cannanas API request failed."
        return result

    def _build_body_request_kwargs(self, operation: OperationSpec, body: Any) -> dict[str, Any]:
        if body is None:
            return {}

        content_types = {
            str(content_type).lower()
            for content_type in (operation.request_body or {}).get("content_types", [])
        }
        if "application/json" in content_types or not content_types:
            return {"json": body}
        if "application/x-www-form-urlencoded" in content_types:
            if isinstance(body, dict):
                return {"data": self._flatten_query_params(body)}
            return {"data": {"body": body}}
        if "multipart/form-data" in content_types:
            return self._build_multipart_request_kwargs(body)
        if "text/plain" in content_types:
            if isinstance(body, str):
                return {"content": body.encode("utf-8"), "headers": {"Content-Type": "text/plain; charset=utf-8"}}
            return {
                "content": json.dumps(body, ensure_ascii=False).encode("utf-8"),
                "headers": {"Content-Type": "text/plain; charset=utf-8"},
            }
        return {"json": body}

    def _build_multipart_request_kwargs(self, body: Any) -> dict[str, Any]:
        if not isinstance(body, dict):
            return {"files": [("body", (None, json.dumps(body, ensure_ascii=False)))]}

        files: list[tuple[str, Any]] = []
        for key, value in body.items():
            file_tuple = self._coerce_file_tuple(value)
            if file_tuple is not None:
                files.append((key, file_tuple))
                continue
            if isinstance(value, (dict, list)):
                files.append((key, (None, json.dumps(value, ensure_ascii=False))))
            else:
                files.append((key, (None, str(value))))
        return {"files": files}

    def _coerce_file_tuple(self, value: Any) -> tuple[Any, ...] | None:
        if not isinstance(value, dict):
            return None

        filename = value.get("filename") or value.get("name") or "upload.bin"
        content_type = value.get("content_type") or value.get("mime_type") or "application/octet-stream"
        if "content_base64" in value:
            raw = base64.b64decode(value["content_base64"])
            return (filename, raw, content_type)
        if "content" in value:
            content = value["content"]
            if isinstance(content, bytes):
                raw = content
            elif isinstance(content, str):
                raw = content.encode("utf-8")
            else:
                raw = json.dumps(content, ensure_ascii=False).encode("utf-8")
            return (filename, raw, content_type)
        return None

    def extract_list_items(self, data: Any) -> list[dict[str, Any]]:
        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]
        if not isinstance(data, dict):
            return []
        for key in self.LIST_CONTAINER_KEYS:
            value = data.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        list_values = [value for value in data.values() if isinstance(value, list)]
        if len(list_values) == 1:
            return [item for item in list_values[0] if isinstance(item, dict)]
        return []

    def _flatten_query_params(self, query_params: dict[str, Any]) -> dict[str, Any]:
        flattened: dict[str, Any] = {}
        for key, value in query_params.items():
            if value is None:
                continue
            flattened[key] = value
        return flattened
