# Macrobond Plugin for GitHub Copilot CLI

Query economic and financial time-series data from [Macrobond](https://www.macrobond.com/) directly in GitHub Copilot CLI.

## Features

- **Search** for economic indicators (CPI, GDP, unemployment, yields, FX, commodities)
- **Fetch** time series with metadata and observations
- **Revision history** — query point-in-time data, track how statistics were revised
- **Cross-country sets** — build comparable datasets across regions
- **MCP Server** — bundled and automatically started when you install the plugin

## Requirements

- [Macrobond](https://www.macrobond.com/) account with API access
- GitHub Copilot CLI
- Python 3.10+ with `pip`

## Installation

### Step 1: Install Python dependencies

The bundled MCP server requires `requests` and `fastmcp`:

```bash
pip install requests fastmcp
```

### Step 2: Set environment variables

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

### Step 3: Install the plugin

```bash
copilot plugin install mb-ne/copilot-plugin
```

The MCP server starts automatically when Copilot CLI needs it — no manual server management required.

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

The plugin bundles a Python MCP server (`server.py`) that talks to the Macrobond Web API. When Copilot CLI invokes a Macrobond tool, it spawns the server as a local subprocess over stdio — no network endpoint or port needed. OAuth tokens are fetched and cached automatically; credentials are passed via environment variables.

## License

Proprietary - Macrobond Financial AB — see [LICENCE](LICENCE)
