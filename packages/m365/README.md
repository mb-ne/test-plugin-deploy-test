# Macrobond for Microsoft 365 Copilot

Search and retrieve economic time series data from Macrobond. Use the agent in
Microsoft 365 Copilot to compare indicators and create charts and tables without
leaving the conversation.

## Requirements

- A [Microsoft 365 Copilot license](https://learn.microsoft.com/microsoft-365-copilot/extensibility/prerequisites#prerequisites)
- Permission to upload custom apps in your Microsoft 365 tenant
- An active Macrobond AI Data Feed subscription and a Macrobond account

Your Teams administrator controls whether custom apps can be uploaded and who can
install them.

## Install

### 1. Download the app package

Download the
[latest Macrobond app package](https://github.com/macrobond-platform/macrobond-plugins/releases/latest/download/Macrobond-AI-Data-Feed-M365-Copilot-Agent.zip).
Do not unzip it; Microsoft expects the ZIP as downloaded.

To install a specific version or roll back, choose a versioned package from the
[Macrobond plugin releases](https://github.com/macrobond-platform/macrobond-plugins/releases).

### 2. Upload it to Microsoft 365

For tenant-wide availability, open the Teams admin center and go to
**Teams apps → Manage apps → Actions → Upload new app**. Select the downloaded ZIP
and approve it. Microsoft documents the complete process in
[Upload a custom app](https://learn.microsoft.com/microsoftteams/upload-custom-apps).

To install it only for yourself, open Microsoft 365 Copilot or Teams and go to
**Apps → Manage your apps → Upload an app → Upload a custom app**. This option is
available only when your administrator permits custom-app uploads.

### 3. Connect your Macrobond account

Open Copilot, select **Macrobond** from the agent list, and ask it a question.
Copilot prompts you to sign in to Macrobond the first time it needs data and
remembers the connection afterwards.

## Try it

- _"Give me a chart of Sweden GDP."_
- _"Compare US and euro area core inflation over the last ten years."_
- _"Show me a table of German unemployment, monthly, since 2020."_
- _"What was US GDP growth as first reported, versus the current figure?"_

## Changelog

See [`CHANGELOG.md`](CHANGELOG.md).

## License

See [`LICENCE`](LICENCE).
