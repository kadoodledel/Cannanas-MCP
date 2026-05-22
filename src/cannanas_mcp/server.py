from __future__ import annotations

from functools import lru_cache
from typing import Any

from fastmcp import FastMCP
from fastmcp.apps import AppConfig, ResourceCSP

from cannanas_mcp.dashboard import DASHBOARD_URI, dashboard_html
from cannanas_mcp.client import CannanasClient
from cannanas_mcp.config import Settings, load_settings
from cannanas_mcp.openapi_index import OperationIndex


mcp = FastMCP("Cannanas MCP Server")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return load_settings()


@lru_cache(maxsize=1)
def get_index() -> OperationIndex:
    settings = get_settings()
    return OperationIndex.from_file(settings.openapi_path)


def _missing_api_key_error() -> dict[str, Any]:
    return {
        "ok": False,
        "error": "Missing Cannanas API key. Set CANNANAS_API_KEY in the MCP server environment before calling Cannanas endpoints.",
    }


def _dashboard_summary() -> dict[str, Any]:
    settings = get_settings()
    index = get_index()
    featured_operations = index.search(limit=8, include_unsupported=False)
    return {
        "ok": True,
        "server": {
            "name": "Cannanas MCP Server",
            "base_url": settings.api_base_url,
            "openapi_path": str(settings.openapi_path),
            "transport": settings.transport,
            "api_key_configured": bool(settings.api_key),
            "operations_indexed": len(index.operations),
            "dashboard_uri": DASHBOARD_URI,
        },
        "highlights": {
            "tags": index.tags(),
            "featured_operation_count": len(featured_operations),
        },
        "featured_operations": featured_operations,
        "quick_start": [
            "Search operations by intent, tag, or method.",
            "Inspect an operation before calling it.",
            "Run the auth test to confirm your API key works.",
            "Use the reporting tools for weekly metrics by club.",
        ],
    }


@mcp.resource("cannanas://info")
def server_info() -> dict[str, Any]:
    settings = get_settings()
    index = get_index()
    return {
        "name": "Cannanas MCP Server",
        "base_url": settings.api_base_url,
        "openapi_path": str(settings.openapi_path),
        "operations_indexed": len(index.operations),
        "tags": index.tags(),
        "dashboard_uri": DASHBOARD_URI,
        "tools": [
            "cannanas_dashboard",
            "search_operations",
            "describe_operation",
            "auth_test",
            "call_operation",
        ],
    }


@mcp.tool(
    app=AppConfig(
        resource_uri=DASHBOARD_URI,
        csp=ResourceCSP(resource_domains=["https://unpkg.com"]),
    )
)
def cannanas_dashboard() -> dict[str, Any]:
    """Open the Cannanas control room app."""
    return _dashboard_summary()


@mcp.resource(
    DASHBOARD_URI,
    app=AppConfig(
        csp=ResourceCSP(resource_domains=["https://unpkg.com"]),
    ),
)
def dashboard_view() -> str:
    return dashboard_html()


@mcp.tool
def search_operations(
    query: str = "",
    tag: str | None = None,
    method: str | None = None,
    limit: int = 15,
    include_unsupported: bool = False,
) -> dict[str, Any]:
    """Search Cannanas API operations by free text, tag, or HTTP method."""
    index = get_index()
    results = index.search(
        query=query,
        tag=tag,
        method=method,
        limit=max(1, min(limit, 50)),
        include_unsupported=include_unsupported,
    )
    return {
        "query": query,
        "tag": tag,
        "method": method,
        "count": len(results),
        "results": results,
    }


@mcp.tool
def describe_operation(operation_id: str) -> dict[str, Any]:
    """Return the full input shape for a Cannanas API operation before you call it."""
    operation = get_index().get(operation_id)
    return operation.to_detail()


@mcp.tool
async def auth_test() -> dict[str, Any]:
    """Call Cannanas /v1/auth/test using the configured CANNANAS_API_KEY."""
    settings = get_settings()
    if not settings.api_key:
        return _missing_api_key_error()

    operation = get_index().get("testAuth")
    client = CannanasClient(
        base_url=settings.api_base_url,
        api_key=settings.api_key,
        timeout_seconds=settings.timeout_seconds,
    )
    rendered_path = get_index().render_path(operation, {})
    return await client.call_operation(operation=operation, rendered_path=rendered_path)


@mcp.tool
async def call_operation(
    operation_id: str,
    path_params: dict[str, Any] | None = None,
    query_params: dict[str, Any] | None = None,
    body: dict[str, Any] | list[Any] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Call a supported Cannanas API operation by operation_id."""
    settings = get_settings()
    if not settings.api_key:
        return _missing_api_key_error()

    operation = get_index().get(operation_id)
    if not operation.supported:
        return {
            "ok": False,
            "error": operation.unsupported_reason,
            "operation": operation.to_summary(),
        }

    rendered_path = get_index().render_path(operation, path_params)
    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "operation": operation.to_summary(),
            "rendered_path": rendered_path,
            "query_params": query_params,
            "body": body,
        }

    client = CannanasClient(
        base_url=settings.api_base_url,
        api_key=settings.api_key,
        timeout_seconds=settings.timeout_seconds,
    )
    return await client.call_operation(
        operation=operation,
        rendered_path=rendered_path,
        query_params=query_params,
        body=body,
    )


def main() -> None:
    mcp.run(transport=get_settings().transport)
