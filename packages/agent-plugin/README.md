# Macrobond for Agent Plugins

Search and retrieve economic time series data from Macrobond. Use this package in
clients that support the Agent Plugins 1.0 format.

This package includes the Macrobond skill and configures the hosted Macrobond MCP
service.

## Requirements

- An active Macrobond AI Data Feed subscription and a Macrobond account
- A compatible Agent Plugins client

## Install

### VS Code

Run **Chat: Install Plugin From Source** and select this directory. For a local
checkout, you can also add its absolute path to `chat.pluginLocations`.

### Cursor

Use the dedicated [Cursor package](../cursor) instead. It carries the sign-in
configuration Cursor needs.

### GitHub Copilot CLI

Use the dedicated [GitHub Copilot CLI package](../copilot) instead. It carries
the sign-in configuration Copilot CLI needs.

## Connect your Macrobond account

Ask the client to use Macrobond. If it asks you to sign in, follow the prompt and
use your Macrobond account.

If the client asks for a client ID, enter `macrobond_mcp_search_retrieval`. The
Agent Plugins 1.0 format has no field for it.

## Try it

- *"Give me a chart of Sweden GDP."*
- *"Compare US and euro area core inflation over the last ten years."*
- *"Show me a table of German unemployment, monthly, since 2020."*

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md).

## License

See [`LICENCE`](LICENCE).
