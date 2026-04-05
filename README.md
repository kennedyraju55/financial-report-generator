<div align="center">
<img src="https://img.shields.io/badge/💰_Financial_Report_Generator-Local_LLM_Powered-blue?style=for-the-badge&labelColor=1a1a2e&color=16213e" alt="Project Banner" width="600"/>
<br/>
<img src="https://img.shields.io/badge/Gemma_4-Ollama-orange?style=flat-square&logo=google&logoColor=white" alt="Gemma 4"/>
<img src="https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/Streamlit-Web_UI-red?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"/>
<img src="https://img.shields.io/badge/Click-CLI-green?style=flat-square&logo=gnu-bash&logoColor=white" alt="Click CLI"/>
<img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="License"/>
<br/><br/>
<strong>Part of <a href="https://github.com/kennedyraju55/90-local-llm-projects">90 Local LLM Projects</a> collection</strong>
</div>
<br/>

# 💰 Financial Report Generator

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/tests-pytest-orange.svg)](tests/)

> **Production-grade** financial reporting system powered by local LLMs. Generate board-ready narrative reports, ratio analysis, forecasts, and period comparisons from CSV data — all from the CLI or a Streamlit web UI.

---

## 📐 Architecture

```
47-financial-report-generator/
├── src/financial_reporter/
│   ├── __init__.py          # Package metadata & version
│   ├── core.py              # 🧠 Business logic (metrics, ratios, LLM narratives)
│   ├── cli.py               # ⌨️  Click CLI interface
│   └── web_ui.py            # 🌐 Streamlit web dashboard
├── tests/
│   ├── test_core.py         # Core logic tests
│   └── test_cli.py          # CLI integration tests
├── config.yaml              # ⚙️  Configuration (model, ratios, forecast)
├── setup.py                 # Package installer
├── Makefile                 # Dev shortcuts
├── requirements.txt         # Dependencies
├── .env.example             # Environment template
└── README.md                # You are here
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📊 **Auto Metrics** | Totals, averages, min/max, latest for every numeric column |
| 📈 **Ratio Analysis** | Profit margin, expense ratio, growth rate, operating margin |
| 🔮 **Forecasting** | Linear trend projection for N periods ahead |
| 🔄 **Period Comparison** | Side-by-side current vs previous period with % changes |
| 📝 **Narrative Reports** | LLM-generated board-ready financial reports |
| 💼 **Executive Summary** | Concise CFO-style overview via LLM |
| 💵 **Cash Flow Analysis** | Treasury-focused cash flow narrative |
| ⌨️ **Rich CLI** | Beautiful terminal output with tables, panels, and color |
| 🌐 **Web Dashboard** | Streamlit UI with upload, charts, and metric cards |
| ⚙️ **Config-Driven** | YAML configuration for model, ratios, forecast, currency |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **[Ollama](https://ollama.ai/)** running locally with the Gemma 3 model:
  ```bash
  ollama pull gemma3
  ollama serve
  ```

### Installation

```bash
# Clone and install
cd 47-financial-report-generator
pip install -r requirements.txt

# Or install as a package
pip install -e .
```

### Prepare Your Data

Create a CSV file with financial columns:

```csv
month,revenue,expenses,net_income
October,500000,350000,150000
November,550000,380000,170000
December,600000,400000,200000
```

---

## ⌨️ CLI Usage

The CLI provides four commands: `report`, `summary`, `ratios`, and `forecast`.

```bash
# Full financial report
python -m src.financial_reporter.cli report -f financials.csv -p Q4-2024

# Executive summary only
python -m src.financial_reporter.cli report -f financials.csv -p Q4-2024 --summary

# Executive summary (shortcut command)
python -m src.financial_reporter.cli summary -f financials.csv -p Q4-2024

# Ratio analysis
python -m src.financial_reporter.cli ratios -f financials.csv

# Forecast next 5 periods
python -m src.financial_reporter.cli forecast -f financials.csv -n 5

# Use custom config
python -m src.financial_reporter.cli -c my_config.yaml report -f data.csv -p Q1-2025
```

### CLI Output Example

```
💰 Financial Report Generator — Q4-2024
✓ Loaded 3 records from financials.csv

┌────────────────────┬──────────────┬──────────────┬──────────────┐
│ Metric             │        Total │      Average │       Latest │
├────────────────────┼──────────────┼──────────────┼──────────────┤
│ revenue            │ $1,650,000   │   $550,000   │   $600,000   │
│ expenses           │ $1,130,000   │   $376,667   │   $400,000   │
│ net_income         │   $520,000   │   $173,333   │   $200,000   │
└────────────────────┴──────────────┴──────────────┴──────────────┘

╭── 📋 Financial Report — Q4-2024 ──╮
│ # Executive Summary                │
│ Q4-2024 showed strong growth...    │
╰────────────────────────────────────╯
```

---

## 🌐 Web UI Usage

Launch the Streamlit dashboard:

```bash
streamlit run src/financial_reporter/web_ui.py
```

### Web UI Tabs

| Tab | What It Does |
|-----|-------------|
| 📂 **Data Upload** | Upload CSV, preview data table |
| 📝 **Report Sections** | Generate executive summary, income analysis, cash flow |
| 📊 **Ratio Cards** | `st.metric` cards for profit margin, expense ratio, growth |
| 📈 **Period Comparison** | Bar charts comparing periods, trend lines |

---

## ⚙️ Configuration Guide

All settings live in `config.yaml`:

```yaml
model:
  name: "gemma3"           # Ollama model name
  temperature: 0.3         # LLM creativity (0.0 = deterministic)
  max_tokens: 4000         # Max response length

report_sections:           # Sections included in full report
  - executive_summary
  - revenue_analysis
  - expense_analysis
  - ratio_analysis
  - cash_flow
  - forecast
  - recommendations

ratios:                    # Which ratios to compute
  profit_margin: true
  expense_ratio: true
  revenue_growth: true
  operating_margin: true

forecast:
  periods_ahead: 3         # Number of future periods
  method: "linear"         # Forecasting method

currency: "USD"
currency_symbol: "$"

logging:
  level: "INFO"
  file: "financial_reporter.log"
```

### Environment Variables

Copy `.env.example` to `.env` and customise:

```bash
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=gemma3
LOG_LEVEL=INFO
CONFIG_PATH=config.yaml
CURRENCY=USD
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=src/financial_reporter --cov-report=term-missing

# Using Makefile
make test
```

---

## 🛠️ Development

```bash
# Install dev dependencies
make dev

# Run linter
make lint

# Clean caches
make clean
```

---

## 📚 API Reference

### Core Functions (`src.financial_reporter.core`)

| Function | Description |
|----------|-------------|
| `load_config(path)` | Load YAML config with defaults |
| `load_financial_data(file_path)` | Parse CSV → list of dicts |
| `safe_float(val)` | Currency/percent-safe float conversion |
| `compute_financial_metrics(data)` | Total, avg, min, max, latest per column |
| `compute_ratios(metrics)` | Profit margin, expense ratio, growth rate |
| `compare_periods(data, current, previous)` | Period-over-period comparison |
| `forecast_metrics(data, periods_ahead)` | Linear trend projection |
| `compute_analytics(data, metrics)` | Bundle metrics + ratios + forecast |
| `generate_financial_report(data, metrics, period)` | Full LLM narrative report |
| `generate_executive_summary(metrics, period)` | Brief executive summary |
| `generate_cash_flow_narrative(data, metrics)` | Cash flow analysis |

---

## 📸 Screenshots

> _Screenshots will be added once the application UI is finalized._

<!-- Add your screenshots here:
![Dashboard](docs/screenshots/dashboard.png)
![Analysis Results](docs/screenshots/results.png)
-->


---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
