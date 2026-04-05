<div align="center">

<!-- Banner -->
<img src="docs/images/banner.svg" alt="Financial Report Generator Banner" width="800"/>

<br/><br/>

<!-- Badges -->
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Ollama](https://img.shields.io/badge/Ollama-gemma3-fb8500?style=for-the-badge&logo=llama&logoColor=white)](https://ollama.ai/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web_UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Click CLI](https://img.shields.io/badge/Click-CLI-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)](https://click.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-ffb703?style=for-the-badge)](LICENSE)

<br/>

[![Tests](https://img.shields.io/github/actions/workflow/status/kennedyraju55/financial-report-generator/tests.yml?label=tests&style=flat-square&logo=pytest)](https://github.com/kennedyraju55/financial-report-generator/actions)
[![GitHub stars](https://img.shields.io/github/stars/kennedyraju55/financial-report-generator?style=flat-square&color=fb8500)](https://github.com/kennedyraju55/financial-report-generator/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/kennedyraju55/financial-report-generator?style=flat-square)](https://github.com/kennedyraju55/financial-report-generator/issues)
[![GitHub last commit](https://img.shields.io/github/last-commit/kennedyraju55/financial-report-generator?style=flat-square&color=fb8500)](https://github.com/kennedyraju55/financial-report-generator/commits/master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)]()

<br/>

**Production-grade financial reporting powered by local LLMs.**
<br/>
Generate board-ready narrative reports, ratio analysis, forecasts, and period comparisons — all from CSV data, entirely offline.

<br/>

**Part of the [90 Local LLM Projects](https://github.com/kennedyraju55/90-local-llm-projects) collection**

<br/>

[Features](#-features) · [Quick Start](#-quick-start) · [CLI Usage](#-cli-reference) · [Web UI](#-web-ui) · [Architecture](#-architecture) · [API Reference](#-api-reference) · [Config](#%EF%B8%8F-configuration) · [FAQ](#-faq) · [Contributing](#-contributing)

</div>

---

## 🤔 Why Financial Report Generator?

| Problem | Our Solution |
|---------|-------------|
| Financial reports take hours to write manually | **LLM generates board-ready narratives in seconds** |
| Cloud AI tools expose sensitive financial data | **100% local — your data never leaves your machine** |
| Spreadsheets don't provide narrative analysis | **AI-powered insights with proper financial terminology** |
| Ratio calculations are error-prone by hand | **Automated profit margin, expense ratio, growth rate, operating margin** |
| No easy way to forecast future periods | **Built-in linear regression forecasting for N periods ahead** |
| Comparing periods requires manual work | **Automatic period-over-period comparison with absolute & percentage changes** |
| Different stakeholders need different reports | **Full report, executive summary, and cash flow narrative — one tool** |
| Setting up data pipelines is complex | **Drop a CSV → get professional reports instantly** |

---

## ✨ Features

<div align="center">
<img src="docs/images/features.svg" alt="Core Features" width="800"/>
</div>

<br/>

### 📊 Financial Metrics Engine

Automatically computes **total**, **average**, **min**, **max**, and **latest** values for every numeric column in your dataset. Handles currency symbols (`$`), percentage signs (`%`), and comma-separated numbers seamlessly via the `safe_float()` parser.

```python
from src.financial_reporter.core import compute_financial_metrics

metrics = compute_financial_metrics(data)
# {
#   "revenue":    {"total": 1650000, "average": 550000, "min": 500000, "max": 600000, "latest": 600000},
#   "expenses":   {"total": 1130000, "average": 376667, "min": 350000, "max": 400000, "latest": 400000},
#   "net_income": {"total":  520000, "average": 173333, "min": 150000, "max": 200000, "latest": 200000}
# }
```

### 📈 Ratio Analysis

Computes four key financial ratios when `revenue`, `expenses`, and `net_income` columns are present:

| Ratio | Formula | What It Tells You |
|-------|---------|-------------------|
| **Profit Margin** | `net_income / revenue` | How much profit per dollar of revenue |
| **Expense Ratio** | `expenses / revenue` | Cost efficiency — lower is better |
| **Operating Margin** | `(revenue - expenses) / revenue` | Operational profitability |
| **Growth Rate** | `(latest_revenue - min_revenue) / min_revenue` | Revenue trajectory over the dataset |

### 🔮 Linear Regression Forecasting

Projects future values using least-squares linear regression (`y = mx + b`) where `x` is the row index. Configure the number of forecast periods via CLI flag or `config.yaml`.

### 🔄 Period-over-Period Comparison

Compare any two labeled periods in your data with:
- **Absolute change** — raw difference in totals
- **Percentage change** — proportional shift for each metric column

### 🤖 LLM-Powered Report Generation

Three distinct report types, each powered by a tailored system prompt:

| Report Type | Persona | Output |
|-------------|---------|--------|
| **Full Financial Report** | Senior Financial Analyst & CPA | 6-section board-ready narrative with executive summary, revenue/expense analysis, ratios, comparison, outlook |
| **Executive Summary** | Chief Financial Officer (CFO) | Concise 3-paragraph overview highlighting key figures and trends |
| **Cash Flow Narrative** | Treasury Analyst | Cash flow analysis focused on inflows, outflows, net position, and liquidity |

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| **Python** | 3.10+ | Runtime |
| **Ollama** | Latest | Local LLM inference |
| **gemma3** model | — | Default language model |

### 1. Install Ollama & Pull the Model

```bash
# Install Ollama (see https://ollama.ai for platform-specific instructions)
# Then pull the model and start the server:
ollama pull gemma3
ollama serve
```

### 2. Clone & Install

```bash
git clone https://github.com/kennedyraju55/financial-report-generator.git
cd financial-report-generator

# Install dependencies
pip install -r requirements.txt

# Or install as an editable package
pip install -e .
```

### 3. Prepare Financial Data

Create a CSV file with numeric financial columns:

```csv
month,revenue,expenses,net_income,cash_flow
January,$1200000,$840000,$360000,$280000
February,$1350000,$890000,$460000,$350000
March,$1500000,$950000,$550000,$420000
April,$1280000,$870000,$410000,$310000
May,$1600000,$980000,$620000,$490000
June,$1750000,$1020000,$730000,$580000
```

> 💡 **Tip:** Columns can include `$`, `%`, and commas — the `safe_float()` parser strips them automatically.

### 4. Generate Your First Report

```bash
# Full narrative report
python -m src.financial_reporter.cli report -f financials.csv -p Q2-2024

# Quick executive summary
python -m src.financial_reporter.cli report -f financials.csv -p Q2-2024 --summary
```

### Expected Output

```
╭─ 💰 Financial Report Generator — Q2-2024 ─╮
╰────────────────────────────────────────────╯
✓ Loaded 6 records from financials.csv

┌──────────────────────────────────────────────────────────────────┐
│                    💰 Financial Data Summary                     │
├────────────────────┬──────────────┬──────────────┬──────────────┤
│ Metric             │        Total │      Average │       Latest │
├────────────────────┼──────────────┼──────────────┼──────────────┤
│ revenue            │ $8,680,000   │ $1,446,667   │ $1,750,000   │
│ expenses           │ $5,550,000   │   $925,000   │ $1,020,000   │
│ net_income         │ $3,130,000   │   $521,667   │   $730,000   │
│ cash_flow          │ $2,430,000   │   $405,000   │   $580,000   │
└────────────────────┴──────────────┴──────────────┴──────────────┘

╭── 📋 Financial Report — Q2-2024 ──────────────────────────────────╮
│                                                                    │
│  # Executive Summary                                               │
│                                                                    │
│  Q2-2024 demonstrated robust financial performance with total      │
│  revenue of $8.68M, representing consistent month-over-month       │
│  growth. Net income reached $3.13M with a healthy profit margin    │
│  of 36.1%, reflecting strong operational efficiency...             │
│                                                                    │
│  ## Revenue & Income Analysis                                      │
│  ...                                                               │
╰────────────────────────────────────────────────────────────────────╯
```


## 🐳 Docker Deployment

Run this project instantly with Docker — no local Python setup needed!

### Quick Start with Docker

```bash
# Clone and start
git clone https://github.com/kennedyraju55/financial-report-generator.git
cd financial-report-generator
docker compose up

# Access the web UI
open http://localhost:8501
```

### Docker Commands

| Command | Description |
|---------|-------------|
| `docker compose up` | Start app + Ollama |
| `docker compose up -d` | Start in background |
| `docker compose down` | Stop all services |
| `docker compose logs -f` | View live logs |
| `docker compose build --no-cache` | Rebuild from scratch |

### Architecture

```
┌─────────────────┐     ┌─────────────────┐
│   Streamlit UI  │────▶│   Ollama + LLM  │
│   Port 8501     │     │   Port 11434    │
└─────────────────┘     └─────────────────┘
```

> **Note:** First run will download the Gemma 4 model (~5GB). Subsequent starts are instant.

---


---


---

## ⚡ REST API

Every project includes a FastAPI REST API with auto-generated docs.

### Start the API Server

```bash
# Run directly
uvicorn src.financial_reporter.api:app --reload --port 8000

# Or with Docker
docker compose up
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/docs` | Interactive Swagger UI |
| `GET` | `/redoc` | ReDoc documentation |
| `POST` | `/analyze` | Main analysis endpoint |

### Example Request

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "your input here"}'
```

> 📖 Visit `http://localhost:8000/docs` for the full interactive API documentation.

## ⌨️ CLI Reference

The CLI is built with [Click](https://click.palletsprojects.com/) and uses [Rich](https://rich.readthedocs.io/) for beautiful terminal output.

### Global Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--config` | `-c` | `config.yaml` | Path to YAML configuration file |

### Commands

#### `report` — Generate Financial Report

```bash
python -m src.financial_reporter.cli report [OPTIONS]
```

| Option | Short | Required | Default | Description |
|--------|-------|----------|---------|-------------|
| `--file` | `-f` | ✅ | — | Path to financial data CSV |
| `--period` | `-p` | ✅ | — | Reporting period label (e.g., `Q4-2024`) |
| `--full / --summary` | — | ❌ | `--full` | Generate full report or executive summary only |

**Examples:**

```bash
# Full report with all sections
python -m src.financial_reporter.cli report -f data.csv -p Q4-2024

# Executive summary only
python -m src.financial_reporter.cli report -f data.csv -p Q4-2024 --summary

# Custom config file
python -m src.financial_reporter.cli -c prod_config.yaml report -f data.csv -p FY-2024
```

#### `summary` — Executive Summary

```bash
python -m src.financial_reporter.cli summary [OPTIONS]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--file` | `-f` | ✅ | Path to financial data CSV |
| `--period` | `-p` | ✅ | Reporting period label |

```bash
python -m src.financial_reporter.cli summary -f quarterly.csv -p Q1-2025
```

#### `ratios` — Financial Ratio Analysis

```bash
python -m src.financial_reporter.cli ratios [OPTIONS]
```

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--file` | `-f` | ✅ | Path to financial data CSV |

**Example Output:**

```
┌──────────────────────────────────────────┐
│          📊 Financial Ratio Analysis      │
├──────────────────────┬───────────────────┤
│ Ratio                │             Value │
├──────────────────────┼───────────────────┤
│ Profit Margin        │            36.06% │
│ Expense Ratio        │            63.94% │
│ Operating Margin     │            36.06% │
│ Growth Rate          │            45.83% │
└──────────────────────┴───────────────────┘
```

#### `forecast` — Financial Forecasting

```bash
python -m src.financial_reporter.cli forecast [OPTIONS]
```

| Option | Short | Required | Default | Description |
|--------|-------|----------|---------|-------------|
| `--file` | `-f` | ✅ | — | Path to financial data CSV |
| `--periods` | `-n` | ❌ | `3` | Number of future periods to project |

**Example Output:**

```
┌──────────────────────────────────────────────────────────────┐
│                   🔮 Financial Forecast                       │
├────────────────────┬──────────────┬──────────────┬───────────┤
│ Metric             │    Period +1 │    Period +2 │ Period +3 │
├────────────────────┼──────────────┼──────────────┼───────────┤
│ revenue            │ $1,825,714   │ $1,928,571   │$2,031,429 │
│ expenses           │ $1,062,857   │ $1,095,714   │$1,128,571 │
│ net_income         │   $762,857   │   $832,857   │  $902,857 │
│ cash_flow          │   $612,857   │   $672,857   │  $732,857 │
└────────────────────┴──────────────┴──────────────┴───────────┘
```

### Using Makefile Shortcuts

```bash
# Run CLI with arguments
make run-cli ARGS="report -f data.csv -p Q4-2024"
make run-cli ARGS="ratios -f data.csv"
make run-cli ARGS="forecast -f data.csv -n 5"
```

---

## 🌐 Web UI

The Streamlit web dashboard provides a full graphical interface for all features.

### Launch

```bash
# Direct launch
streamlit run src/financial_reporter/web_ui.py

# Via Makefile
make run-web
```

The app opens at `http://localhost:8501` by default.

### Dashboard Tabs

| Tab | Description | Key Features |
|-----|-------------|-------------|
| 📂 **Data Upload** | Upload CSV & preview data | Drag-and-drop file upload, full data table preview, row/column counts |
| 📝 **Report Sections** | Generate LLM-powered reports | Three report buttons: Executive Summary, Income Analysis, Cash Flow |
| 📊 **Ratio Cards** | Visual ratio display | `st.metric` cards for profit margin, expense ratio, operating margin, growth rate |
| 📈 **Period Comparison** | Compare & visualize periods | Period selector dropdowns, bar charts of % changes, trend line charts |

### Web UI Features

- **Sidebar:** File uploader, period input field, report type radio selector
- **Session State:** Data persists across tabs after upload — no need to re-upload
- **Auto-detection:** Automatically identifies period/label columns for comparison
- **Numeric Detection:** `pandas` dtype-based column filtering for chart generation
- **Ollama Check:** Verifies Ollama connectivity before attempting LLM generation

---

## 🏗️ Architecture

<div align="center">
<img src="docs/images/architecture.svg" alt="System Architecture" width="800"/>
</div>

<br/>

### Data Flow

```
Financial CSV → Data Parser → Metric Engine → ┬─→ Ratio Calculator ───────┐
                                               ├─→ Period Comparator ──────┤
                                               └─→ Forecast Engine ────────┤
                                                                           ↓
                                                               LLM Report Generator
                                                                     │
                                              ┌──────────────────────┼──────────────────────┐
                                              ↓                      ↓                      ↓
                                     Executive Summary         Full Report          Cash Flow Narrative
```

### Project Structure

```
47-financial-report-generator/
├── src/
│   └── financial_reporter/
│       ├── __init__.py              # Package metadata & version
│       ├── core.py                  # 🧠 Business logic
│       │   ├── load_config()        #    YAML configuration loader
│       │   ├── safe_float()         #    Currency/percent-safe conversion
│       │   ├── load_financial_data()#    CSV parser
│       │   ├── compute_financial_metrics()  # Metric aggregation
│       │   ├── compute_ratios()     #    Financial ratio computation
│       │   ├── compare_periods()    #    Period-over-period comparison
│       │   ├── forecast_metrics()   #    Linear regression forecasting
│       │   ├── compute_analytics()  #    Analytics bundler
│       │   ├── generate_financial_report()  # Full LLM narrative
│       │   ├── generate_executive_summary() # Concise LLM summary
│       │   └── generate_cash_flow_narrative()# Cash flow LLM narrative
│       ├── cli.py                   # ⌨️  Click CLI interface
│       │   ├── main (group)         #    CLI entry point with --config
│       │   ├── report               #    Full report / summary command
│       │   ├── summary              #    Executive summary command
│       │   ├── ratios               #    Ratio analysis command
│       │   └── forecast             #    Forecasting command
│       └── web_ui.py               # 🌐 Streamlit web dashboard
│           ├── Data Upload tab      #    CSV upload & preview
│           ├── Report Sections tab  #    LLM report generation
│           ├── Ratio Cards tab      #    Financial ratio display
│           └── Period Comparison tab #    Charts & comparisons
├── tests/
│   ├── __init__.py
│   ├── test_core.py                 # Core logic unit tests
│   └── test_cli.py                  # CLI integration tests
├── common/                          # Shared LLM client library
│   └── llm_client.py               # Ollama API wrapper (chat, check)
├── docs/
│   └── images/
│       ├── banner.svg               # Project banner
│       ├── architecture.svg         # Architecture diagram
│       └── features.svg             # Feature grid
├── config.yaml                      # ⚙️  Default configuration
├── setup.py                         # Package installer (pip install -e .)
├── Makefile                         # Dev shortcuts (test, lint, run, clean)
├── requirements.txt                 # Production + dev dependencies
├── .env.example                     # Environment variable template
└── README.md                        # This file
```

### Module Dependencies

```
cli.py ──────→ core.py ──────→ common/llm_client.py ──────→ Ollama API
                  ↑
web_ui.py ────────┘
                  ↑
config.yaml ──────┘  (loaded via load_config())
```

---

## 📚 API Reference

### `core.py` — Core Business Logic

#### Configuration

```python
from src.financial_reporter.core import load_config

# Load with defaults
config = load_config()

# Load from custom YAML (deep-merges with defaults)
config = load_config("config.yaml")
```

**`load_config(path: Optional[str] = None) → dict`**

Loads configuration from a YAML file. Missing keys fall back to `DEFAULT_CONFIG`. Uses recursive deep-merge so partial overrides work correctly.

---

#### Data Loading

```python
from src.financial_reporter.core import safe_float, load_financial_data

# safe_float handles currency symbols, percentages, and commas
safe_float("$1,234.56")   # → 1234.56
safe_float("85.5%")       # → 85.5
safe_float("N/A")         # → 0.0

# Load CSV as list of dictionaries
data = load_financial_data("financials.csv")
# [{"month": "Jan", "revenue": "500000", ...}, ...]
```

**`safe_float(val: Any) → float`**

Strips `$`, `%`, and `,` from the input, then converts to float. Returns `0.0` for non-convertible values.

**`load_financial_data(file_path: str) → list[dict]`**

Reads a CSV file using `csv.DictReader`. Raises `FileNotFoundError` if the file doesn't exist, `ValueError` if empty or unparseable.

---

#### Metric Computation

```python
from src.financial_reporter.core import compute_financial_metrics

metrics = compute_financial_metrics(data)
# Returns: {"column_name": {"total": ..., "average": ..., "min": ..., "max": ..., "latest": ...}}
```

**`compute_financial_metrics(data: list[dict]) → dict`**

Iterates over every column in the dataset. For columns where at least one value is non-zero and the first row's value is convertible to float, computes five aggregations: `total`, `average`, `min`, `max`, `latest`.

---

#### Ratio Analysis

```python
from src.financial_reporter.core import compute_ratios

ratios = compute_ratios(metrics)
# {"profit_margin": 0.36, "expense_ratio": 0.64, "operating_margin": 0.36, "growth_rate": 0.46}
```

**`compute_ratios(metrics: dict) → dict`**

Requires `revenue`, `expenses`, and/or `net_income` keys in the metrics dictionary. Returns ratios as proportions (not percentages).

---

#### Period Comparison

```python
from src.financial_reporter.core import compare_periods

result = compare_periods(data, "Q2-2024", "Q1-2024")
# {
#   "current":  {"revenue": {"total": ...}, ...},
#   "previous": {"revenue": {"total": ...}, ...},
#   "changes":  {"revenue": {"absolute": 150000, "percentage": 12.5}, ...}
# }
```

**`compare_periods(data: list[dict], current_period: str, previous_period: str) → dict`**

Searches all string columns for matching period labels (case-insensitive). Computes metrics for each period, then calculates absolute and percentage changes.

---

#### Forecasting

```python
from src.financial_reporter.core import forecast_metrics

forecasts = forecast_metrics(data, periods_ahead=3)
# {"revenue": [1825714.29, 1928571.43, 2031428.57], "expenses": [...], ...}
```

**`forecast_metrics(data: list[dict], periods_ahead: int = 3) → dict`**

Uses least-squares linear regression where `x` is the row index. Projects `periods_ahead` future values for each numeric column.

---

#### Analytics Bundle

```python
from src.financial_reporter.core import compute_analytics

analytics = compute_analytics(data, metrics)
# {"metrics": {...}, "ratios": {...}, "forecast": {...}}
```

**`compute_analytics(data: list[dict], metrics: dict) → dict`**

Convenience function that bundles `metrics`, `compute_ratios(metrics)`, and `forecast_metrics(data)` into a single dictionary.

---

#### LLM Report Generation

```python
from src.financial_reporter.core import (
    generate_financial_report,
    generate_executive_summary,
    generate_cash_flow_narrative,
)

# Full 6-section narrative report (Senior Financial Analyst persona)
full_report = generate_financial_report(data, metrics, "Q4-2024")

# Concise 3-paragraph executive summary (CFO persona)
summary = generate_executive_summary(metrics, "Q4-2024")

# Cash flow focused analysis (Treasury Analyst persona)
cash_flow = generate_cash_flow_narrative(data, metrics)
```

Each function constructs a tailored system prompt and user message, then calls the local LLM via `common.llm_client.chat()`. Reports are returned as Markdown strings.

---

## ⚙️ Configuration

### `config.yaml` — Full Reference

```yaml
# ─── LLM Model Settings ───────────────────────────────────────────
model:
  name: "gemma3"              # Ollama model name (gemma3, llama3, mistral, etc.)
  temperature: 0.3            # LLM creativity (0.0 = deterministic, 1.0 = creative)
  max_tokens: 4000            # Maximum response length in tokens

# ─── Report Structure ─────────────────────────────────────────────
report_sections:              # Sections included in full financial report
  - executive_summary         # High-level overview
  - revenue_analysis          # Revenue trends and breakdown
  - expense_analysis          # Cost structure and efficiency
  - ratio_analysis            # Financial ratios and indicators
  - cash_flow                 # Cash position and liquidity
  - forecast                  # Forward-looking projections
  - recommendations           # Strategic recommendations

# ─── Ratio Configuration ──────────────────────────────────────────
ratios:
  profit_margin: true         # net_income / revenue
  expense_ratio: true         # expenses / revenue
  revenue_growth: true        # (latest - min) / min
  operating_margin: true      # (revenue - expenses) / revenue

# ─── Forecast Settings ────────────────────────────────────────────
forecast:
  periods_ahead: 3            # Number of future periods to project
  method: "linear"            # Forecasting method (linear regression)

# ─── Currency Display ─────────────────────────────────────────────
currency: "USD"               # ISO 4217 currency code
currency_symbol: "$"          # Symbol used in formatted output

# ─── Logging ───────────────────────────────────────────────────────
logging:
  level: "INFO"               # DEBUG, INFO, WARNING, ERROR, CRITICAL
  file: "financial_reporter.log"  # Log file path
```

### Environment Variables

Copy `.env.example` to `.env`:

```bash
# Ollama connection
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=gemma3

# Application settings
LOG_LEVEL=INFO
CONFIG_PATH=config.yaml
CURRENCY=USD
```

### Switching Models

To use a different Ollama model, update `config.yaml`:

```yaml
model:
  name: "llama3"        # or "mistral", "codellama", "phi3", etc.
  temperature: 0.3
  max_tokens: 4000
```

Then pull the model:

```bash
ollama pull llama3
```

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=src/financial_reporter --cov-report=term-missing

# Run specific test file
pytest tests/test_core.py -v
pytest tests/test_cli.py -v

# Run with short traceback
pytest tests/ -v --tb=short

# Using Makefile shortcut
make test
```

### Test Structure

| File | Tests | What It Covers |
|------|-------|----------------|
| `test_core.py` | Core logic | `safe_float`, `load_financial_data`, `compute_financial_metrics`, `compute_ratios`, `compare_periods`, `forecast_metrics`, `compute_analytics` |
| `test_cli.py` | CLI integration | Click command invocation, option parsing, output format, error handling |

---

## 🏠 Local LLM vs Cloud — Why Local?

| Aspect | Local (Ollama) | Cloud (OpenAI, etc.) |
|--------|---------------|---------------------|
| **Data Privacy** | ✅ Data never leaves your machine | ❌ Sent to third-party servers |
| **Cost** | ✅ Free after hardware | ❌ Per-token pricing |
| **Latency** | ⚡ No network round-trip | 🐌 Depends on API latency |
| **Availability** | ✅ Works offline | ❌ Requires internet |
| **Financial Compliance** | ✅ SOX/GDPR friendly | ⚠️ May violate data policies |
| **Customization** | ✅ Fine-tune locally | ⚠️ Limited model options |
| **Hardware** | ⚠️ Needs decent GPU/CPU | ✅ Runs anywhere |

> 💡 For financial data that may contain sensitive revenue figures, salaries, or client information, local LLM inference is the **safest choice**.

---

## ❓ FAQ

<details>
<summary><strong>1. What CSV format does the tool expect?</strong></summary>

Any CSV with headers. The tool automatically detects numeric columns by attempting `float()` conversion (after stripping `$`, `%`, `,`). Non-numeric columns are preserved as labels for period comparison. Example:

```csv
quarter,revenue,expenses,net_income
Q1-2024,$1200000,$840000,$360000
Q2-2024,$1500000,$950000,$550000
```

</details>

<details>
<summary><strong>2. Which Ollama models work best for financial reports?</strong></summary>

The default `gemma3` works well for structured financial analysis. Other good options:

| Model | Size | Quality | Speed |
|-------|------|---------|-------|
| `gemma3` | 4B | ⭐⭐⭐⭐ | Fast |
| `llama3` | 8B | ⭐⭐⭐⭐⭐ | Medium |
| `mistral` | 7B | ⭐⭐⭐⭐ | Medium |
| `phi3` | 3.8B | ⭐⭐⭐ | Very Fast |

Update `config.yaml` → `model.name` to switch models.

</details>

<details>
<summary><strong>3. How does the forecasting algorithm work?</strong></summary>

The tool uses **ordinary least-squares linear regression**:

1. Each row is assigned an index `x = 0, 1, 2, ...`
2. Computes slope `m` and intercept `b` from the data
3. Projects future values: `y = m * (n + j) + b` for `j = 0..periods_ahead-1`

This is a simple trend extrapolation — suitable for data with linear growth patterns. For non-linear data, consider preprocessing or using a more sophisticated model.

</details>

<details>
<summary><strong>4. Can I use this without Ollama / without an LLM?</strong></summary>

Yes! The metrics, ratios, forecasting, and period comparison features work **without any LLM**. Only the narrative report generation commands (`report`, `summary`, and the "Generate" buttons in the Web UI) require Ollama to be running.

```bash
# These work without Ollama:
python -m src.financial_reporter.cli ratios -f data.csv
python -m src.financial_reporter.cli forecast -f data.csv -n 5
```

</details>

<details>
<summary><strong>5. How do I add custom financial ratios?</strong></summary>

Extend the `compute_ratios()` function in `core.py`:

```python
def compute_ratios(metrics: dict) -> dict:
    ratios = {}
    # ... existing ratios ...

    # Add your custom ratio
    assets = metrics.get("total_assets", {})
    liabilities = metrics.get("total_liabilities", {})
    if assets.get("total") and liabilities.get("total"):
        ratios["debt_to_asset"] = liabilities["total"] / assets["total"]

    return ratios
```

Then add the corresponding flag in `config.yaml` under `ratios:`.

</details>

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

### Development Setup

```bash
# 1. Fork & clone
git clone https://github.com/kennedyraju55/financial-report-generator.git
cd financial-report-generator

# 2. Install dev dependencies
make dev
# or manually:
pip install -r requirements.txt
pip install -e ".[dev]"

# 3. Verify tests pass
make test

# 4. Run linter
make lint
```

### Guidelines

1. **Fork** the repository and create a feature branch
2. **Write tests** for new functionality in `tests/`
3. **Follow** existing code style (Black formatting, type hints)
4. **Update** documentation if adding new features
5. **Run** `make test && make lint` before submitting
6. **Submit** a pull request with a clear description

### Makefile Commands

| Command | Description |
|---------|-------------|
| `make install` | Install production dependencies |
| `make dev` | Install dev dependencies + editable package |
| `make test` | Run pytest with coverage |
| `make lint` | Run ruff or flake8 linter |
| `make run-cli ARGS="..."` | Run CLI with arguments |
| `make run-web` | Launch Streamlit web UI |
| `make clean` | Remove `__pycache__`, `.pytest_cache`, build artifacts |

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**💰 Financial Report Generator** — Part of the [90 Local LLM Projects](https://github.com/kennedyraju55/90-local-llm-projects) collection

Built with ❤️ using Python, Click, Rich, Streamlit & Ollama

<br/>

<img src="https://img.shields.io/badge/Project_47-Financial_Report_Generator-fb8500?style=for-the-badge&labelColor=0d1117" alt="Project 47"/>

<br/><br/>

[⬆ Back to Top](#)

</div>
