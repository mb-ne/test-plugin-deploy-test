# Macrobond for Cursor

Search and retrieve economic time series data from Macrobond in Cursor.

This package includes the Macrobond skill and configures the hosted Macrobond MCP
service.

## Requirements

- An active Macrobond AI Data Feed subscription and a Macrobond account
- Cursor 2.5 or later

## Install

Add the Macrobond marketplace and install the plugin:

1. Open **Dashboard → Settings → Plugins**.
2. Under **Team Marketplaces**, select **Import** and enter
   `https://github.com/macrobond-platform/macrobond-plugins`.
3. Install the `macrobond` plugin.

For a local checkout, copy or link this directory to
`~/.cursor/plugins/local/macrobond`, then reload Cursor.

## Connect your Macrobond account

Ask Cursor to use Macrobond. If it asks you to sign in, follow the prompt and use
your Macrobond account.

## Try it

- *"Give me a chart of Sweden GDP."*
- *"Compare US and euro area core inflation over the last ten years."*
- *"Show me a table of German unemployment, monthly, since 2020."*

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md).

## License

See [`LICENCE`](LICENCE).
