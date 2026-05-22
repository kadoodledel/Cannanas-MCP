from __future__ import annotations

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
        if body is not None:
            request_kwargs["json"] = body

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
