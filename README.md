# Macrobond Plugin for GitHub Copilot CLI

Query economic and financial time-series data from [Macrobond](https://www.macrobond.com/) directly in GitHub Copilot CLI.

## Features

- **Search** for economic indicators (CPI, GDP, unemployment, yields, FX, commodities)
- **Fetch** time series with metadata and observations
- **Revision history** — query point-in-time data, track how statistics were revised
- **Cross-country sets** — build comparable datasets across regions
- **Local MCP Server** — starts automatically via stdio, no manual server setup needed

## Requirements

- [Macrobond](https://www.macrobond.com/) account with API access
- GitHub Copilot CLI
- [uv](https://docs.astral.sh/uv/) (Python package runner)

## Installation

### Step 1: Set environment variables

Set your Macrobond API credentials in your shell profile (`~/.bashrc`, `~/.zshrc`, or Windows user environment variables):

```bash
export MACROBOND_CLIENT_ID=your_client_id
export MACROBOND_CLIENT_SECRET=your_client_secret
```

On Windows (PowerShell):

```powershell
[System.Environment]::SetEnvironmentVariable("MACROBOND_CLIENT_ID", "your_client_id", "User")
[System.Environment]::SetEnvironmentVariable("MACROBOND_CLIENT_SECRET", "your_client_secret", "User")
```

### Step 2: Install the plugin

```bash
copilot plugin install mb-ne/copilot-plugin
```

That's it. The MCP server starts automatically when the agent needs it — no manual server management required. Dependencies (`fastmcp`, `requests`) are resolved on the fly by `uv`.

## Usage

Example queries in Copilot CLI:

- "Get US CPI year-over-year data"
- "Find German unemployment rate monthly"
- "Build a G7 inflation comparison"
- "What was US GDP as known on 2020-01-01?"

## Plugin Structure

```
copilot-plugin/
├── plugin.json                              # Plugin manifest
├── .mcp.json                                # MCP server config (local stdio)
├── server.py                                # MCP server entry point
├── macrobond_adapter_http.py                # Macrobond HTTP client
├── requirements.txt                         # Python dependencies
├── .github/
│   ├── plugin/marketplace.json              # Marketplace manifest
│   └── skills/macrobond/
│       ├── SKILL.md                         # Skill instructions
│       └── references/
│           ├── domain_knowledge.md          # Selection rules
│           └── metadata_guide.md            # Filter values
└── LICENCE
```

## How it works

The plugin runs a local MCP server via stdio transport. When the AI agent activates the plugin, it spawns the server process automatically using `uv run`, which handles dependency installation. The server authenticates with the Macrobond API using your credentials from environment variables, manages OAuth tokens, and caches them for the lifetime of the process. No credentials are persisted to disk.

## License

Proprietary - Macrobond Financial AB — see [LICENCE](LICENCE)
