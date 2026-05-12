# Macrobond Plugin for GitHub Copilot CLI

Query economic and financial time-series data from [Macrobond](https://www.macrobond.com/) directly in GitHub Copilot CLI.

## Features

- **Search** for economic indicators (CPI, GDP, unemployment, yields, FX, commodities)
- **Fetch** time series with metadata and observations
- **Revision history** — query point-in-time data, track how statistics were revised
- **Cross-country sets** — build comparable datasets across regions
- **MCP Server** — automatically configured when you install the plugin

## Installation

### Option 1: Install as Plugin (Recommended)

```bash
# Add the marketplace
copilot plugin marketplace add mb-ne/copilot-plugin

# Install the plugin
copilot plugin install macrobond@mb-ne-copilot-plugin
```

### Option 2: Manual Clone

```bash
git clone https://github.com/mb-ne/copilot-plugin.git
copilot plugin install ./copilot-plugin
```

## Configuration

Set these environment variables before using the plugin:

```bash
export MACROBOND_MCP_URL=https://mcp.macrobond.com/sse
export MACROBOND_API_KEY=your_api_key_here
```

Add them to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.) to persist across sessions.

## Usage

Invoke with: `/macrobond`

Example queries:
- "Get US CPI year-over-year data"
- "Find German unemployment rate monthly"
- "Build a G7 inflation comparison"
- "What was US GDP as known on 2020-01-01?"

## Plugin Structure

```
copilot-plugin/
├── plugin.json                              # Plugin manifest
├── .mcp.json                                # MCP server config
├── .github/
│   ├── plugin/marketplace.json              # Marketplace manifest
│   └── skills/macrobond/
│       ├── SKILL.md                         # Skill instructions
│       └── references/
│           ├── domain_knowledge.md          # Selection rules
│           └── metadata_guide.md            # Filter values
└── LICENCE
```

## Requirements

- [Macrobond](https://www.macrobond.com/) account with API access
- GitHub Copilot CLI

## License

Proprietary - Macrobond Financial AB — see [LICENCE](LICENCE)
