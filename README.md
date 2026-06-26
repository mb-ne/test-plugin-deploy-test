# macrobond-plugin

Plugin that provides the `/macrobond` skill for Claude Code and GitHub Copilot CLI. Used together with `macrobond-mcp` — the skill provides the instructions and context for the AI agent, while the MCP server (deployed remotely) provides the tools it calls. The plugin ships a `.mcp.json` that configures the client to connect to the remote server; the server itself is not bundled.

## Table of contents

- [Install from marketplace](#install-from-marketplace)
  - [Requirements](#requirements)
  - [Claude Code](#claude-code)
  - [GitHub Copilot CLI](#github-copilot-cli)
- [Install from ZIP](#install-from-zip)
  - [Requirements](#requirements-1)
  - [Claude Code](#claude-code-1)
  - [GitHub Copilot CLI](#github-copilot-cli-1)
- [License](#license)

## Install from marketplace

### Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/getting-started) or [GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli/about-github-copilot-in-the-cli)
- [Git](https://git-scm.com/downloads)
- Internet access to GitHub

### Claude Code

```
/plugin marketplace add macrobond-platform/macrobond-plugins
/plugin install macrobond@macrobond-plugins
```

### GitHub Copilot CLI

```
/plugin marketplace add macrobond-platform/macrobond-plugins
/plugin install macrobond@macrobond-plugins
```

## Install from ZIP

To install the plugin from a ZIP file, download the ZIP, unzip it to a folder of your choice, and follow the steps below.

- [Latest release](https://github.com/macrobond-platform/macrobond-plugins/releases/latest) *(recommended)*
- [All releases](https://github.com/macrobond-platform/macrobond-plugins/releases)

### Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/getting-started) or [GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli/about-github-copilot-in-the-cli)

### Claude Code

```
/plugin marketplace add <path-to-extracted-folder>
/plugin install macrobond@macrobond-plugins
```

### GitHub Copilot CLI

```
/plugin marketplace add <path-to-extracted-folder>
/plugin install macrobond@macrobond-plugins
```

### License

See [LICENCE](plugins/macrobond/skills/macrobond/LICENCE).

