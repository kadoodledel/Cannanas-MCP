from __future__ import annotations


DASHBOARD_URI = "ui://cannanas/dashboard.html"


def dashboard_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="color-scheme" content="dark light" />
  <title>Cannanas Control Room</title>
  <style>
    :root {
      --bg: #08111f;
      --bg-soft: rgba(11, 18, 32, 0.82);
      --panel: rgba(15, 23, 42, 0.86);
      --panel-strong: rgba(17, 24, 39, 0.96);
      --border: rgba(148, 163, 184, 0.18);
      --text: #e5eefc;
      --muted: #9db0cb;
      --accent: #f9a826;
      --accent-2: #30d5c8;
      --accent-3: #7dd3fc;
      --danger: #fb7185;
      --success: #34d399;
      --shadow: 0 24px 80px rgba(2, 6, 23, 0.45);
      --radius: 22px;
      --radius-sm: 14px;
      font-synthesis: none;
      text-rendering: optimizeLegibility;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    * { box-sizing: border-box; }

    html, body {
      margin: 0;
      min-height: 100%;
      background:
        radial-gradient(circle at top left, rgba(249, 168, 38, 0.16), transparent 26%),
        radial-gradient(circle at top right, rgba(48, 213, 200, 0.14), transparent 22%),
        linear-gradient(180deg, #07101d 0%, #0a1220 42%, #050915 100%);
      color: var(--text);
      font-family: "Segoe UI", "Aptos", "Avenir Next", "Helvetica Neue", system-ui, sans-serif;
    }

    body {
      padding: 18px;
    }

    .shell {
      position: relative;
      overflow: hidden;
      max-width: 1280px;
      margin: 0 auto;
      border: 1px solid rgba(148, 163, 184, 0.16);
      border-radius: 28px;
      background: linear-gradient(180deg, rgba(7, 16, 29, 0.86), rgba(4, 10, 20, 0.94));
      box-shadow: var(--shadow);
    }

    .shell::before,
    .shell::after {
      content: "";
      position: absolute;
      border-radius: 999px;
      pointer-events: none;
      filter: blur(8px);
      opacity: 0.9;
    }

    .shell::before {
      inset: 22px auto auto -140px;
      width: 260px;
      height: 260px;
      background: radial-gradient(circle, rgba(249, 168, 38, 0.2), transparent 66%);
    }

    .shell::after {
      inset: auto -120px 24px auto;
      width: 300px;
      height: 300px;
      background: radial-gradient(circle, rgba(48, 213, 200, 0.16), transparent 68%);
    }

    .layout {
      position: relative;
      display: grid;
      grid-template-columns: minmax(0, 1.5fr) minmax(320px, 0.9fr);
      gap: 18px;
      padding: 20px;
    }

    .hero,
    .panel,
    .card,
    .metric,
    .result {
      backdrop-filter: blur(18px);
      -webkit-backdrop-filter: blur(18px);
      background: var(--bg-soft);
      border: 1px solid var(--border);
      border-radius: var(--radius);
    }

    .hero {
      padding: 24px;
      background:
        linear-gradient(135deg, rgba(15, 23, 42, 0.92), rgba(9, 16, 29, 0.72)),
        linear-gradient(135deg, rgba(249, 168, 38, 0.09), rgba(48, 213, 200, 0.05));
    }

    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 7px 12px;
      border-radius: 999px;
      background: rgba(249, 168, 38, 0.12);
      color: #ffd592;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    .title {
      margin: 14px 0 10px;
      font-size: clamp(34px, 5vw, 58px);
      line-height: 0.96;
      letter-spacing: -0.05em;
    }

    .subtitle {
      max-width: 72ch;
      margin: 0;
      color: var(--muted);
      font-size: 15px;
      line-height: 1.65;
    }

    .meta-row {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 18px;
    }

    .chip {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 9px 12px;
      border-radius: 999px;
      background: rgba(148, 163, 184, 0.08);
      color: var(--text);
      border: 1px solid rgba(148, 163, 184, 0.14);
      font-size: 13px;
    }

    .chip strong { color: white; }

    .grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin-top: 18px;
    }

    .metric {
      padding: 14px;
      min-height: 98px;
    }

    .metric .label {
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    .metric .value {
      margin-top: 8px;
      font-size: 26px;
      font-weight: 800;
      letter-spacing: -0.03em;
    }

    .metric .hint {
      margin-top: 8px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.4;
    }

    .panel {
      padding: 18px;
    }

    .panel + .panel {
      margin-top: 18px;
    }

    .panel-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 14px;
    }

    .panel-title {
      margin: 0;
      font-size: 16px;
      letter-spacing: -0.02em;
    }

    .panel-subtitle {
      margin: 4px 0 0;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.5;
    }

    .toolbar {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }

    button,
    input,
    select {
      font: inherit;
    }

    button {
      appearance: none;
      border: 0;
      cursor: pointer;
      transition: transform 140ms ease, opacity 140ms ease, box-shadow 140ms ease;
    }

    button:hover { transform: translateY(-1px); }
    button:active { transform: translateY(0); opacity: 0.92; }

    .btn-primary,
    .btn-secondary,
    .btn-ghost {
      padding: 11px 14px;
      border-radius: 14px;
      font-weight: 700;
    }

    .btn-primary {
      color: #09111d;
      background: linear-gradient(135deg, #ffd26f, #f9a826);
      box-shadow: 0 10px 28px rgba(249, 168, 38, 0.24);
    }

    .btn-secondary {
      color: var(--text);
      background: rgba(148, 163, 184, 0.08);
      border: 1px solid rgba(148, 163, 184, 0.16);
    }

    .btn-ghost {
      color: var(--muted);
      background: transparent;
      border: 1px dashed rgba(148, 163, 184, 0.18);
    }

    .field-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
    }

    .field,
    .select-field {
      width: 100%;
      padding: 11px 12px;
      color: var(--text);
      background: rgba(5, 10, 20, 0.72);
      border: 1px solid rgba(148, 163, 184, 0.16);
      border-radius: 14px;
      outline: none;
    }

    .field::placeholder {
      color: #6f86a7;
    }

    .field:focus,
    .select-field:focus {
      border-color: rgba(48, 213, 200, 0.55);
      box-shadow: 0 0 0 4px rgba(48, 213, 200, 0.12);
    }

    .select-field {
      appearance: none;
    }

    .results {
      display: grid;
      gap: 12px;
    }

    .result {
      padding: 15px;
      cursor: pointer;
      transition: transform 140ms ease, border-color 140ms ease, background 140ms ease;
    }

    .result:hover {
      transform: translateY(-1px);
      border-color: rgba(249, 168, 38, 0.42);
      background: rgba(15, 23, 42, 0.96);
    }

    .result-top {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
      justify-content: space-between;
    }

    .result-id {
      font-size: 14px;
      font-weight: 800;
      letter-spacing: -0.01em;
    }

    .result-summary {
      margin-top: 6px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.5;
    }

    .result-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 10px;
    }

    .tag {
      display: inline-flex;
      align-items: center;
      padding: 5px 8px;
      border-radius: 999px;
      background: rgba(125, 211, 252, 0.1);
      color: #c2edff;
      border: 1px solid rgba(125, 211, 252, 0.18);
      font-size: 12px;
    }

    .detail {
      margin-top: 14px;
      padding-top: 14px;
      border-top: 1px solid rgba(148, 163, 184, 0.12);
    }

    .detail pre,
    .panel pre {
      margin: 0;
      white-space: pre-wrap;
      word-break: break-word;
      color: #dbeafe;
      font-size: 12px;
      line-height: 1.55;
    }

    .status-line {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
      color: var(--muted);
      font-size: 13px;
    }

    .status {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(148, 163, 184, 0.08);
      border: 1px solid rgba(148, 163, 184, 0.14);
      color: var(--text);
    }

    .status-dot {
      width: 10px;
      height: 10px;
      border-radius: 999px;
      background: var(--success);
      box-shadow: 0 0 0 4px rgba(52, 211, 153, 0.12);
    }

    .status-dot.warn {
      background: var(--accent);
      box-shadow: 0 0 0 4px rgba(249, 168, 38, 0.12);
    }

    .status-dot.bad {
      background: var(--danger);
      box-shadow: 0 0 0 4px rgba(251, 113, 133, 0.12);
    }

    .kicker {
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 8px;
    }

    .stack {
      display: grid;
      gap: 12px;
    }

    .mini-note {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.55;
    }

    .footer-note {
      margin-top: 16px;
      color: #7691b2;
      font-size: 12px;
      line-height: 1.5;
    }

    @media (max-width: 1080px) {
      .layout {
        grid-template-columns: 1fr;
      }

      .grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }

      .field-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }

    @media (max-width: 720px) {
      body {
        padding: 10px;
      }

      .shell {
        border-radius: 22px;
      }

      .layout,
      .hero,
      .panel {
        padding-left: 14px;
        padding-right: 14px;
      }

      .grid,
      .field-grid {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <div class="shell">
    <div class="layout">
      <main>
        <section class="hero">
          <div class="eyebrow">Cannanas Control Room</div>
          <h1 class="title">Search the Cannanas API, inspect operations, and launch reporting workflows from one app.</h1>
          <p class="subtitle">
            This MCP App turns the Cannanas OpenAPI spec into a guided workspace for support, ops, and reporting.
            Use it to discover endpoints, inspect payload shapes, run auth checks, and explore the server's available tools.
          </p>

          <div class="meta-row" id="meta-row"></div>

          <div class="grid" id="metrics"></div>
        </section>

        <section class="panel">
          <div class="panel-head">
            <div>
              <h2 class="panel-title">Operation search</h2>
              <p class="panel-subtitle">Find an operation by intent, tag, or HTTP method, then jump into its schema.</p>
            </div>
            <div class="toolbar">
              <button class="btn-secondary" id="refresh-dashboard" type="button">Refresh dashboard</button>
            </div>
          </div>

          <div class="field-grid">
            <input class="field" id="search-query" placeholder="Try: charges, carts, members" />
            <input class="field" id="search-tag" placeholder="Tag filter" />
            <select class="select-field" id="search-method">
              <option value="">Any method</option>
              <option>GET</option>
              <option>POST</option>
              <option>PUT</option>
              <option>PATCH</option>
              <option>DELETE</option>
            </select>
            <button class="btn-primary" id="run-search" type="button">Search</button>
          </div>

          <div class="footer-note">Search results are clickable. Select one to load its operation details below.</div>
        </section>

        <section class="panel">
          <div class="panel-head">
            <div>
              <h2 class="panel-title">Results</h2>
              <p class="panel-subtitle">Your latest search, dashboard payload, or tool output appears here.</p>
            </div>
          </div>
          <div class="results" id="results"></div>
        </section>
      </main>

      <aside>
        <section class="panel">
          <div class="panel-head">
            <div>
              <h2 class="panel-title">Quick actions</h2>
              <p class="panel-subtitle">Common workflows for a Cannanas support or operations session.</p>
            </div>
          </div>

          <div class="stack">
            <div class="toolbar">
              <button class="btn-primary" id="auth-test" type="button">Run auth test</button>
              <button class="btn-secondary" id="load-featured" type="button">Load featured operations</button>
            </div>

            <div class="panel" style="padding: 14px; background: rgba(148, 163, 184, 0.05);">
              <div class="kicker">Weekly metrics</div>
              <div class="field-grid" style="grid-template-columns: 1fr 1fr;">
                <input class="field" id="club-id" placeholder="Club ID" />
                <input class="field" id="metrics-start" type="date" />
                <input class="field" id="metrics-end" type="date" />
                <button class="btn-primary" id="run-metrics" type="button">Get metrics</button>
              </div>
              <div class="footer-note">Populate these dates to pull the reporting bundle for a specific club.</div>
            </div>

            <div class="panel" style="padding: 14px; background: rgba(148, 163, 184, 0.05);">
              <div class="kicker">Server context</div>
              <pre id="server-context">Waiting for the host to deliver the dashboard payload...</pre>
            </div>
          </div>
        </section>
      </aside>
    </div>
  </div>

  <script type="module">
    import { App } from "https://unpkg.com/@modelcontextprotocol/ext-apps@0.4.0/app-with-deps";

    const app = new App({ name: "Cannanas Control Room", version: "1.0.0" });

    const state = {
      dashboard: null,
      lastSearch: [],
      selectedOperation: null,
    };

    const els = {
      metaRow: document.getElementById("meta-row"),
      metrics: document.getElementById("metrics"),
      results: document.getElementById("results"),
      serverContext: document.getElementById("server-context"),
      query: document.getElementById("search-query"),
      tag: document.getElementById("search-tag"),
      method: document.getElementById("search-method"),
      clubId: document.getElementById("club-id"),
      metricsStart: document.getElementById("metrics-start"),
      metricsEnd: document.getElementById("metrics-end"),
      refreshDashboard: document.getElementById("refresh-dashboard"),
      runSearch: document.getElementById("run-search"),
      authTest: document.getElementById("auth-test"),
      loadFeatured: document.getElementById("load-featured"),
      runMetrics: document.getElementById("run-metrics"),
    };

    function todayISO() {
      return new Date().toISOString().slice(0, 10);
    }

    function daysAgoISO(days) {
      const d = new Date();
      d.setDate(d.getDate() - days);
      return d.toISOString().slice(0, 10);
    }

    els.metricsStart.value = daysAgoISO(6);
    els.metricsEnd.value = todayISO();

    function payloadFromResult(result) {
      if (!result) return null;
      if (typeof result.structuredContent === "object" && result.structuredContent !== null) {
        return result.structuredContent;
      }
      const textBlock = (result.content || []).find((entry) => entry && entry.type === "text" && typeof entry.text === "string");
      if (!textBlock) return result;
      try {
        return JSON.parse(textBlock.text);
      } catch {
        return { text: textBlock.text };
      }
    }

    function pretty(value) {
      return JSON.stringify(value, null, 2);
    }

    function setStatus(message, tone = "ok") {
      const dotClass = tone === "warn" ? "status-dot warn" : tone === "bad" ? "status-dot bad" : "status-dot";
      els.serverContext.innerHTML = `<span class="status"><span class="${dotClass}"></span>${message}</span>`;
    }

    function renderMeta(payload) {
      const items = [];
      const apiKey = payload?.server?.api_key_configured ? "Configured" : "Not set";
      const transport = payload?.server?.transport || "stdio";
      const count = payload?.server?.operations_indexed ?? 0;
      const tags = Array.isArray(payload?.highlights?.tags) ? payload.highlights.tags.length : 0;

      items.push(`<span class="chip"><strong>Transport</strong> ${transport}</span>`);
      items.push(`<span class="chip"><strong>API key</strong> ${apiKey}</span>`);
      items.push(`<span class="chip"><strong>Operations</strong> ${count}</span>`);
      items.push(`<span class="chip"><strong>Tags</strong> ${tags}</span>`);
      els.metaRow.innerHTML = items.join("");
    }

    function renderMetrics(payload) {
      const items = [
        {
          label: "Indexed operations",
          value: payload?.server?.operations_indexed ?? "0",
          hint: "All documented operations parsed from the Cannanas OpenAPI spec.",
        },
        {
          label: "Featured operations",
          value: Array.isArray(payload?.featured_operations) ? payload.featured_operations.length : "0",
          hint: "The most useful endpoints to start exploring in this host.",
        },
        {
          label: "Available tags",
          value: Array.isArray(payload?.highlights?.tags) ? payload.highlights.tags.length : "0",
          hint: "Useful tags for narrowing the search surface.",
        },
      ];

      els.metrics.innerHTML = items.map((item) => `
        <article class="metric">
          <div class="label">${item.label}</div>
          <div class="value">${item.value}</div>
          <div class="hint">${item.hint}</div>
        </article>
      `).join("");
    }

    function renderDashboard(payload) {
      if (!payload) {
        setStatus("Waiting for dashboard data from the host...", "warn");
        return;
      }

      state.dashboard = payload;
      renderMeta(payload);
      renderMetrics(payload);
      els.serverContext.textContent = pretty(payload.server || payload);
      if (Array.isArray(payload.featured_operations) && payload.featured_operations.length) {
        renderOperationList(payload.featured_operations, "Featured operations");
      } else {
        els.results.innerHTML = "";
      }
      setStatus("Dashboard loaded", "ok");
    }

    function renderOperationList(operations, title) {
      const items = operations || [];
      if (!items.length) {
        els.results.innerHTML = `<div class="mini-note">No operations matched the current search.</div>`;
        return;
      }

      els.results.innerHTML = `
        <div class="mini-note" style="margin-bottom: 6px;">${title}</div>
        ${items.map((operation) => `
          <article class="result" data-operation-id="${escapeHtml(operation.operation_id || "")}">
            <div class="result-top">
              <div class="result-id">${escapeHtml(operation.operation_id || "unknown-operation")}</div>
              <span class="tag">${escapeHtml(operation.method || "N/A")}</span>
            </div>
            <div class="result-summary">${escapeHtml(operation.summary || "No summary provided.")}</div>
            <div class="result-tags">
              ${(operation.tags || []).map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`).join("")}
            </div>
            <div class="footer-note">Click to inspect the full schema.</div>
          </article>
        `).join("")}
      `;

      for (const card of els.results.querySelectorAll("[data-operation-id]")) {
        card.addEventListener("click", () => {
          const operationId = card.getAttribute("data-operation-id");
          if (operationId) {
            inspectOperation(operationId);
          }
        });
      }
    }

    function renderOperationDetail(operation) {
      if (!operation) return;

      state.selectedOperation = operation;
      els.results.insertAdjacentHTML("afterbegin", `
        <article class="result" style="margin-bottom: 12px; border-color: rgba(48, 213, 200, 0.35);">
          <div class="result-top">
            <div class="result-id">${escapeHtml(operation.operation_id || "operation")}</div>
            <span class="tag">${escapeHtml(operation.method || "N/A")}</span>
          </div>
          <div class="result-summary">${escapeHtml(operation.description || operation.summary || "No description available.")}</div>
          <div class="detail">
            <div class="kicker">Parameters</div>
            <pre>${escapeHtml(pretty(operation.parameters || []))}</pre>
          </div>
          <div class="detail">
            <div class="kicker">Request body</div>
            <pre>${escapeHtml(pretty(operation.request_body || null))}</pre>
          </div>
        </article>
      `);
    }

    function escapeHtml(value) {
      return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll("\"", "&quot;")
        .replaceAll("'", "&#39;");
    }

    async function callTool(name, args = {}) {
      setStatus(`Running ${name}...`, "warn");
      const result = await app.callServerTool({ name, arguments: args });
      const payload = payloadFromResult(result);
      setStatus(`${name} complete`, result?.isError ? "bad" : "ok");
      return payload;
    }

    async function inspectOperation(operationId) {
      const payload = await callTool("describe_operation", { operation_id: operationId });
      const operation = payload?.operation_id ? payload : payload?.operation;
      if (!operation) {
        els.results.insertAdjacentHTML("afterbegin", `<div class="mini-note">Could not load operation details.</div>`);
        return;
      }
      renderOperationDetail(operation);
      els.serverContext.textContent = pretty(operation);
    }

    els.refreshDashboard.addEventListener("click", async () => {
      const payload = await callTool("cannanas_dashboard");
      renderDashboard(payload);
    });

    els.loadFeatured.addEventListener("click", () => {
      if (state.dashboard?.featured_operations) {
        renderOperationList(state.dashboard.featured_operations, "Featured operations");
      }
    });

    els.runSearch.addEventListener("click", async () => {
      const payload = await callTool("search_operations", {
        query: els.query.value || "",
        tag: els.tag.value || null,
        method: els.method.value || null,
        limit: 12,
      });
      const results = Array.isArray(payload?.results) ? payload.results : [];
      state.lastSearch = results;
      renderOperationList(results, `Search results for "${els.query.value || "all operations"}"`);
      if (payload) {
        els.serverContext.textContent = pretty(payload);
      }
    });

    els.authTest.addEventListener("click", async () => {
      const payload = await callTool("auth_test");
      els.results.innerHTML = `<article class="result"><div class="result-id">Auth test</div><pre>${escapeHtml(pretty(payload))}</pre></article>`;
      els.serverContext.textContent = pretty(payload);
    });

    els.runMetrics.addEventListener("click", async () => {
      if (!els.clubId.value) {
        setStatus("Add a club ID to run reporting metrics.", "warn");
        return;
      }
      const payload = await callTool("get_weekly_metrics", {
        club_id: els.clubId.value,
        start_date: els.metricsStart.value || null,
        end_date: els.metricsEnd.value || null,
      });
      els.results.innerHTML = `<article class="result"><div class="result-id">Weekly metrics</div><pre>${escapeHtml(pretty(payload))}</pre></article>`;
      els.serverContext.textContent = pretty(payload);
    });

    app.ontoolresult = (result) => {
      const payload = payloadFromResult(result);
      if (!payload) return;

      if (payload.server || payload.featured_operations) {
        renderDashboard(payload);
        return;
      }

      if (payload.results && Array.isArray(payload.results)) {
        state.lastSearch = payload.results;
        renderOperationList(payload.results, "Search results");
        els.serverContext.textContent = pretty(payload);
        return;
      }

      if (payload.operation_id) {
        renderOperationDetail(payload);
        els.serverContext.textContent = pretty(payload);
        return;
      }

      els.serverContext.textContent = pretty(payload);
    };

    app.onhostcontextchanged = () => {};

    await app.connect();
  </script>
</body>
</html>
"""
