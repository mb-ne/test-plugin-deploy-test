# Macrobond plugins

Bring trusted economic and financial time-series data from Macrobond into your AI
assistant or coding environment.

The packages in this repository connect supported clients to the hosted Macrobond
MCP service and include a shared skill that teaches the assistant how to search
for series, explain selections, and retrieve data safely.

## Choose your client

| Client | Package | Installation guide |
| --- | --- | --- |
| VS Code | Agent Plugin | [`packages/agent-plugin`](packages/agent-plugin) |
| Cursor | Cursor | [`packages/cursor`](packages/cursor) |
| GitHub Copilot CLI | GitHub Copilot CLI | [`packages/copilot`](packages/copilot) |
| Claude Code, Claude chat, and Cowork | Claude | [`packages/claude`](packages/claude) |
| ChatGPT and Codex | Codex | [`packages/codex`](packages/codex) |
| Gemini CLI | Gemini | [`packages/gemini`](packages/gemini) |
| Microsoft 365 Copilot | Microsoft 365 | [`packages/m365`](packages/m365) |

## What you can do

- Find economic and financial indicators using natural language.
- Retrieve time series with their metadata and source information.
- Compare indicators across countries, concepts, and time periods.
- Create clear charts and tables for research and analysis.
- Explore data revisions and historical releases.

For example:

- *"Give me a chart of Sweden GDP."*
- *"Compare US and euro area core inflation over the last ten years."*
- *"Show me a table of German unemployment, monthly, since 2020."*

## What you need

You need an active Macrobond AI Data Feed subscription, a Macrobond account, and
a supported client. When prompted, sign in with your Macrobond account.

## Repository contents

- [`packages/`](packages) contains the packages for each supported client.
- `.agents/`, `.claude-plugin/`, `.cursor-plugin/`, and `.github/` contain the marketplace
  definitions used by their respective clients.
- [`CHANGELOG.md`](CHANGELOG.md) contains the release history.
- [`LICENCE`](LICENCE) contains the package licence.
