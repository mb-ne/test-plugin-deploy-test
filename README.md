# Macrobond Data Skill for GitHub Copilot

Query economic and financial time-series data from [Macrobond](https://www.macrobond.com/) directly in GitHub Copilot.

## Features

- **Search** for economic indicators (CPI, GDP, unemployment, yields, FX, commodities)
- **Fetch** time series with metadata and observations
- **Revision history** — query point-in-time data, track how statistics were revised
- **Cross-country sets** — build comparable datasets across regions

## Installation

1. **Clone this folder** into your project:
   ```bash
   git clone https://github.com/macrobond/macrobond-data-skill.git
   cp -r macrobond-data-skill/copilot/* your-project/
   ```

2. **Add your credentials** to `.env`:
   ```
   MACROBOND_API_USER_ID=your_username
   MACROBOND_API_PASSWORD=your_password
   ```

3. **Install Python dependencies**:
   ```bash
   pip install requests python-dotenv
   ```

4. **The skill** loads automatically from `.github/skills/macrobond/SKILL.md`

## Usage

Invoke with: `/macrobond`

Example queries:
- "Get US CPI year-over-year data"
- "Find German unemployment rate monthly"
- "Build a G7 inflation comparison"
- "What was US GDP as known on 2020-01-01?"

## File Structure

```
your-project/
├── .github/skills/macrobond/SKILL.md           # Skill instructions
├── macrobond_adapter_http.py       # API wrapper
├── domain_knowledge.md             # Selection rules
├── metadata_guide.md               # Filter values
├── auth_and_runtime.md             # Auth details
└── .env                            # Your credentials
```

## Requirements

- [Macrobond](https://www.macrobond.com/) account with API access
- Macrobond Data+ license (for revision history)
- Python 3.8+
- `requests`, `python-dotenv` packages

## License

MIT — see [LICENCE](LICENCE)
