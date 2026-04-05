# Examples for Financial Report Generator

This directory contains example scripts demonstrating how to use this project.

## Quick Demo

```bash
python examples/demo.py
```

## What the Demo Shows

- **`load_config()`** — Load configuration from a YAML file, falling back to defaults.
- **`safe_float()`** — Convert a value to float, stripping currency/percentage symbols.
- **`load_financial_data()`** — Load financial data from a CSV file.
- **`compute_financial_metrics()`** — Compute key financial metrics (total, average, min, max, latest)
- **`compute_ratios()`** — Compute common financial ratios from pre-computed metrics.

## Prerequisites

- Python 3.10+
- Ollama running with Gemma 4 model
- Project dependencies installed (`pip install -e .`)

## Running

From the project root directory:

```bash
# Install the project in development mode
pip install -e .

# Run the demo
python examples/demo.py
```
