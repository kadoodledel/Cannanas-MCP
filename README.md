# Cannanas MCP Server

A small MCP server that turns the Cannanas OpenAPI spec into a practical AI-facing interface.

It does three things well:

- search Cannanas operations by tag, method, or free text
- inspect an operation before calling it
- call supported Cannanas endpoints with your API key

This project is set up to work locally and to deploy on Alpic.

## What it exposes

- `search_operations`
- `describe_operation`
- `auth_test`
- `call_operation`

The server intentionally does not auto-expose every OpenAPI route as its own MCP tool. The Cannanas spec is large, and a curated interface gives LLM clients much better tool selection behavior.

## Environment variables

- `CANNANAS_API_KEY`: your Cannanas personal API key
- `CANNANAS_BASE_URL`: defaults to `https://api.cannanas.club`
- `CANNANAS_OPENAPI_PATH`: optional override for the spec file path
- `CANNANAS_TIMEOUT_SECONDS`: defaults to `45`
- `MCP_TRANSPORT`: defaults to `stdio`

## Local setup

```bash
uv sync
uv run cannanas-mcp
```

To test over HTTP locally instead of stdio:

```bash
MCP_TRANSPORT=streamable-http uv run cannanas-mcp
```

## Alpic deployment

This repository uses a `pyproject.toml` layout, which matches Alpic's default Python build flow.

1. Push this project to GitHub.
2. In Alpic, create a new project and import the repository.
3. Add `CANNANAS_API_KEY` as an environment variable in the target environment.
4. Deploy.

Alpic can run MCP servers from stdio or Streamable HTTP. This server defaults to `stdio`, which Alpic can host behind its public MCP endpoint. If you prefer, set `MCP_TRANSPORT=streamable-http` in Alpic as well.

After deployment, your server will be available on your Alpic endpoint, typically:

- `https://<your-env>.alpic.live/`
- `https://<your-env>.alpic.live/mcp`

## Example usage

Ask an MCP client:

- "Search Cannanas operations for finance reports"
- "Describe the `getClubBatches` operation"
- "Run the Cannanas auth test"
- "Call `getClubCarts` for club `<club-id>` with query params `{ \"page\": 1 }`"
