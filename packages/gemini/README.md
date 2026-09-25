# Macrobond for Gemini CLI

Search and retrieve economic time series data from Macrobond. Use the extension
in Gemini CLI.

This extension includes the Macrobond skill and configures the hosted Macrobond
MCP service.

## Requirements

- An active Macrobond AI Data Feed subscription and a Macrobond account
- Gemini CLI with extension support

## Install from a local checkout

From `code/macrobond-plugin`, run:

```bash
pnpm sync
gemini extensions validate "$PWD/packages/gemini"
gemini extensions link "$PWD/packages/gemini"
```

Restart Gemini CLI after linking, then verify the extension with
`/extensions list`.

## Connect your Macrobond account

Run `/mcp auth macrobond-mcp`, follow the sign-in prompt, and use your Macrobond
account. Use `/mcp` to inspect the connection.

## Try it

- *"Give me a chart of Sweden GDP."*
- *"Compare US and euro area core inflation over the last ten years."*
- *"Show me a table of German unemployment, monthly, since 2020."*

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md).

## License

See [`LICENCE`](LICENCE).
