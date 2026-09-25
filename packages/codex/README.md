# Macrobond for ChatGPT and Codex

Search and retrieve economic time series data from Macrobond. Use the plugin in
Codex, or connect the hosted MCP service directly to ChatGPT.

The Codex plugin includes the Macrobond skill and configures the hosted Macrobond
MCP service.

## Requirements

- An active Macrobond AI Data Feed subscription and a Macrobond account
- Access to plugins in ChatGPT or Codex

## Install

### ChatGPT web (personal)

1. Open **Settings → Security and login** and turn on **Developer mode**.
2. Open **Plugins** and select **Create app**.
3. Enter **Macrobond** as the name and
   `https://platform.macrobond.com/mcp` as the MCP server URL. Keep
   **Authentication** set to **OAuth**.
4. Open **Advanced OAuth settings**, keep **User-Defined OAuth Client** selected,
   and enter `macrobond_mcp_search_retrieval` as the OAuth client ID.
5. Keep **Token endpoint auth method** set to **none**. Select these default
   scopes and clear any others:
   - `macrobond_web_api.read_mb`
   - `macrobond_web_api.search_mb`
   - `macrobond_web_api.search_retrieval_mcp`
6. Turn off **OIDC enabled**, accept the custom-server warning, and select
   **Create**.
7. Select **Sign in with Macrobond** and complete the sign-in flow.
8. Select **Refresh** and confirm that the Macrobond tools are available.

### ChatGPT workspace

A workspace administrator can make Macrobond available to workspace members:

1. Open **Admin → Plugins** and select **Add → Import marketplace**.
2. Enter `https://github.com/macrobond-platform/macrobond-plugins` as the
   source and leave the marketplace path empty.
3. Select **Import marketplace** and authorize GitHub access when prompted.
4. Review the import results, open **Macrobond**, and configure its installation
   policy for the appropriate workspace roles.

The package currently configures the MCP service through `.mcp.json`, so an
imported workspace plugin is available in the ChatGPT desktop app rather than
ChatGPT on the web.

### ChatGPT and Codex desktop

1. Open **Plugins** and select **Add a marketplace**.
2. Enter `macrobond-platform/macrobond-plugins` as the marketplace source.
3. Open the **Macrobond Plugins** marketplace and install **Macrobond**.

### Codex CLI

Add the Macrobond marketplace and install the plugin:

```text
codex plugin marketplace add https://github.com/macrobond-platform/macrobond-plugins.git
codex plugin add macrobond@macrobond-plugins
```

## Connect your Macrobond account

ChatGPT or Codex asks you to connect Macrobond during installation or the first
time you use it. Follow the prompt and sign in with your Macrobond account.

In Codex CLI, you can start the sign-in flow directly:

```text
codex mcp login macrobond-mcp
```

## Try it

- *"Give me a chart of Sweden GDP."*
- *"Compare US and euro area core inflation over the last ten years."*
- *"Show me a table of German unemployment, monthly, since 2020."*

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md).

## License

See [`LICENCE`](LICENCE).
