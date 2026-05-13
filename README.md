# Macrobond Plugin for GitHub Copilot CLI

Query economic and financial time-series data from [Macrobond](https://www.macrobond.com/) directly in GitHub Copilot CLI.

## Features

- **Search** for economic indicators (CPI, GDP, unemployment, yields, FX, commodities)
- **Fetch** time series with metadata and observations
- **Revision history** — query point-in-time data, track how statistics were revised
- **Cross-country sets** — build comparable datasets across regions
- **MCP Server** — connects to a remote Macrobond MCP server

## Requirements

- [Macrobond](https://www.macrobond.com/) account with API access
- GitHub Copilot CLI
- A running Macrobond MCP server (local or hosted)

## Installation

### Step 1: Set environment variables

Set your Macrobond API credentials and MCP server URL in your shell profile (`~/.bashrc`, `~/.zshrc`, or Windows user environment variables):

```bash
export MACROBOND_MCP_URL=http://127.0.0.1:8000/mcp   # URL of your running MCP server
export MACROBOND_CLIENT_ID=your_client_id
export MACROBOND_CLIENT_SECRET=your_client_secret
```

On Windows (PowerShell):

```powershell
[System.Environment]::SetEnvironmentVariable("MACROBOND_MCP_URL", "http://127.0.0.1:8000/mcp", "User")
[System.Environment]::SetEnvironmentVariable("MACROBOND_CLIENT_ID", "your_client_id", "User")
[System.Environment]::SetEnvironmentVariable("MACROBOND_CLIENT_SECRET", "your_client_secret", "User")
```

### Step 2: Start the MCP server

The MCP server is bundled in this plugin. Start it with:

```bash
pip install fastmcp requests
python ~/.copilot/installed-plugins/mb-ne-copilot-plugin/macrobond/server.py
```

Or for a persistent background process:

```bash
fastmcp run ~/.copilot/installed-plugins/mb-ne-copilot-plugin/macrobond/server.py --transport streamable-http --port 8000
```

The server reads `MACROBOND_CLIENT_ID` and `MACROBOND_CLIENT_SECRET` from environment variables automatically.

### Step 3: Install the plugin

```bash
copilot plugin install mb-ne/copilot-plugin
```

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
├── .mcp.json                                # MCP server config (remote HTTP)
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

The plugin connects Copilot CLI to a Macrobond MCP server over HTTP. The server handles OAuth token management and caches tokens across requests — credentials are never sent through the plugin config, only held by the server process. Multiple users can share a single hosted server instance, each authenticated independently.

## License

Proprietary - Macrobond Financial AB — see [LICENCE](LICENCE)
