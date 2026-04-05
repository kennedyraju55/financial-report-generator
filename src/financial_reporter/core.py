"""
Financial Report Generator - Core Business Logic.

Provides financial data loading, metric computation, ratio analysis,
period comparison, forecasting, and LLM-powered narrative generation.
"""

import csv
import json
import logging
import os
import sys
from typing import Any, Optional

import yaml

# Ensure the common shared library is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from common.llm_client import chat, check_ollama_running

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_CONFIG = {
    "model": {
        "name": "gemma3",
        "temperature": 0.3,
        "max_tokens": 4000,
    },
    "report_sections": [
        "executive_summary",
        "revenue_analysis",
        "expense_analysis",
        "ratio_analysis",
        "cash_flow",
        "forecast",
        "recommendations",
    ],
    "ratios": {
        "profit_margin": True,
        "expense_ratio": True,
        "revenue_growth": True,
        "operating_margin": True,
    },
    "forecast": {
        "periods_ahead": 3,
        "method": "linear",
    },
    "currency": "USD",
    "currency_symbol": "$",
    "logging": {
        "level": "INFO",
        "file": "financial_reporter.log",
    },
}


def load_config(path: Optional[str] = None) -> dict:
    """Load configuration from a YAML file, falling back to defaults.

    Args:
        path: Path to the YAML configuration file.  When *None* or the file
              does not exist the built-in ``DEFAULT_CONFIG`` is returned.

    Returns:
        Merged configuration dictionary.
    """
    config = DEFAULT_CONFIG.copy()
    if path and os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                user_config = yaml.safe_load(fh) or {}
            _deep_merge(config, user_config)
            logger.info("Loaded configuration from %s", path)
        except Exception as exc:
            logger.warning("Failed to load config from %s: %s — using defaults", path, exc)
    else:
        logger.debug("No config file provided or found; using defaults")
    return config


def _deep_merge(base: dict, override: dict) -> None:
    """Recursively merge *override* into *base* in-place."""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------

def safe_float(val: Any) -> float:
    """Convert a value to float, stripping currency/percentage symbols.

    Returns 0.0 for values that cannot be converted.
    """
    try:
        return float(str(val).replace(",", "").replace("$", "").replace("%", ""))
    except (ValueError, TypeError):
        return 0.0


def load_financial_data(file_path: str) -> list[dict]:
    """Load financial data from a CSV file.

    Args:
        file_path: Path to the CSV file.

    Returns:
        List of row dictionaries.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty or cannot be parsed.
    """
    if not os.path.exists(file_path):
        logger.error("File not found: %s", file_path)
        raise FileNotFoundError(f"File '{file_path}' not found.")

    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)
    except Exception as exc:
        logger.error("Error reading CSV %s: %s", file_path, exc)
        raise ValueError(f"Error reading CSV: {exc}") from exc

    if not rows:
        logger.error("CSV file is empty: %s", file_path)
        raise ValueError("CSV file is empty.")

    logger.info("Loaded %d records from %s", len(rows), file_path)
    return rows


# ---------------------------------------------------------------------------
# Metric computation
# ---------------------------------------------------------------------------

def compute_financial_metrics(data: list[dict]) -> dict:
    """Compute key financial metrics (total, average, min, max, latest)
    for every numeric column in the dataset.

    Args:
        data: List of row dictionaries from CSV.

    Returns:
        Dictionary keyed by column name, each value containing
        ``total``, ``average``, ``min``, ``max``, ``latest``.
    """
    if not data:
        logger.warning("No data provided for metric computation")
        return {}

    metrics: dict[str, dict] = {}
    for col in data[0].keys():
        values = [safe_float(row.get(col, 0)) for row in data]
        if not any(v != 0 for v in values):
            continue
        # Verify the first value is actually numeric
        try:
            float(str(data[0][col]).replace(",", "").replace("$", "").replace("%", ""))
        except (ValueError, TypeError):
            continue
        metrics[col] = {
            "total": sum(values),
            "average": sum(values) / len(values) if values else 0,
            "min": min(values),
            "max": max(values),
            "latest": values[-1],
        }

    logger.info("Computed metrics for %d columns", len(metrics))
    return metrics


# ---------------------------------------------------------------------------
# Ratio analysis
# ---------------------------------------------------------------------------

def compute_ratios(metrics: dict) -> dict:
    """Compute common financial ratios from pre-computed metrics.

    Supported ratios (when sufficient data exists):
      - profit_margin: net_income / revenue
      - expense_ratio: expenses / revenue
      - growth_rate: (latest revenue - min revenue) / min revenue
      - operating_margin: (revenue - expenses) / revenue

    Args:
        metrics: Output of :func:`compute_financial_metrics`.

    Returns:
        Dictionary of ratio name → value (as a proportion, *not* percentage).
    """
    ratios: dict[str, float] = {}
    revenue = metrics.get("revenue", {})
    expenses = metrics.get("expenses", {})
    net_income = metrics.get("net_income", {})

    rev_total = revenue.get("total", 0)
    exp_total = expenses.get("total", 0)
    ni_total = net_income.get("total", 0)

    if rev_total:
        ratios["profit_margin"] = ni_total / rev_total
        ratios["expense_ratio"] = exp_total / rev_total
        ratios["operating_margin"] = (rev_total - exp_total) / rev_total

    rev_min = revenue.get("min", 0)
    rev_latest = revenue.get("latest", 0)
    if rev_min and rev_min != 0:
        ratios["growth_rate"] = (rev_latest - rev_min) / rev_min

    logger.info("Computed %d ratios", len(ratios))
    return ratios


# ---------------------------------------------------------------------------
# Period comparison
# ---------------------------------------------------------------------------

def compare_periods(data: list[dict], current_period: str, previous_period: str) -> dict:
    """Compare financial metrics between two periods.

    Each row is expected to have a column whose value matches one of the
    supplied period labels (checks all string columns).

    Args:
        data: Full dataset rows.
        current_period: Label of the current period.
        previous_period: Label of the previous period.

    Returns:
        Dictionary with ``current``, ``previous``, and ``changes`` keys.
        ``changes`` maps each numeric column to its absolute and percentage
        change.
    """
    def _find_period_rows(label: str) -> list[dict]:
        matching: list[dict] = []
        for row in data:
            if any(str(v).strip().lower() == label.strip().lower() for v in row.values()):
                matching.append(row)
        return matching

    current_rows = _find_period_rows(current_period)
    previous_rows = _find_period_rows(previous_period)

    current_metrics = compute_financial_metrics(current_rows) if current_rows else {}
    previous_metrics = compute_financial_metrics(previous_rows) if previous_rows else {}

    changes: dict[str, dict] = {}
    for col in set(list(current_metrics.keys()) + list(previous_metrics.keys())):
        cur_val = current_metrics.get(col, {}).get("total", 0)
        prev_val = previous_metrics.get(col, {}).get("total", 0)
        abs_change = cur_val - prev_val
        pct_change = (abs_change / prev_val * 100) if prev_val else 0
        changes[col] = {"absolute": abs_change, "percentage": pct_change}

    logger.info("Period comparison: %s vs %s — %d columns", current_period, previous_period, len(changes))
    return {
        "current": current_metrics,
        "previous": previous_metrics,
        "changes": changes,
    }


# ---------------------------------------------------------------------------
# Forecasting
# ---------------------------------------------------------------------------

def forecast_metrics(data: list[dict], periods_ahead: int = 3) -> dict:
    """Produce simple linear-trend forecasts for each numeric column.

    Uses the least-squares approach:  ``y = mx + b``  where *x* is the row
    index.

    Args:
        data: Ordered rows of financial data.
        periods_ahead: Number of future periods to project.

    Returns:
        Dictionary keyed by column name → list of forecasted values.
    """
    if not data:
        return {}

    forecasts: dict[str, list[float]] = {}
    n = len(data)

    for col in data[0].keys():
        values = [safe_float(row.get(col, 0)) for row in data]
        # Skip non-numeric columns
        try:
            float(str(data[0][col]).replace(",", "").replace("$", "").replace("%", ""))
        except (ValueError, TypeError):
            continue

        if not any(v != 0 for v in values):
            continue

        # Simple linear regression: y = mx + b
        x_mean = (n - 1) / 2
        y_mean = sum(values) / n
        numerator = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        slope = numerator / denominator if denominator else 0
        intercept = y_mean - slope * x_mean

        projected = [round(slope * (n + j) + intercept, 2) for j in range(periods_ahead)]
        forecasts[col] = projected

    logger.info("Forecasted %d columns for %d periods", len(forecasts), periods_ahead)
    return forecasts


# ---------------------------------------------------------------------------
# Analytics aggregation
# ---------------------------------------------------------------------------

def compute_analytics(data: list[dict], metrics: dict) -> dict:
    """Bundle metrics, ratios, and forecasts into a single analytics dict.

    Args:
        data: Raw financial rows.
        metrics: Pre-computed metrics from :func:`compute_financial_metrics`.

    Returns:
        Dictionary with ``metrics``, ``ratios``, and ``forecast`` keys.
    """
    return {
        "metrics": metrics,
        "ratios": compute_ratios(metrics),
        "forecast": forecast_metrics(data),
    }


# ---------------------------------------------------------------------------
# LLM-powered narrative generation
# ---------------------------------------------------------------------------

def generate_financial_report(data: list[dict], metrics: dict, period: str) -> str:
    """Generate a full narrative financial report via the LLM.

    Args:
        data: Raw financial rows.
        metrics: Pre-computed metrics.
        period: Reporting period label (e.g., ``Q4-2024``).

    Returns:
        Markdown-formatted financial report string.
    """
    data_text = "\n".join(str(row) for row in data[:20])
    metrics_text = json.dumps(metrics, indent=2, default=str)
    ratios = compute_ratios(metrics)
    ratios_text = json.dumps(ratios, indent=2, default=str)

    system_prompt = (
        "You are a senior financial analyst and CPA. Write a professional narrative "
        "financial report suitable for board presentation. Use proper financial "
        "terminology, include specific numbers, and provide insights on performance. "
        "Format with markdown headings, bullet points, and emphasis."
    )

    messages = [
        {
            "role": "user",
            "content": (
                f"Generate a financial report for period: {period}\n\n"
                f"Financial Data:\n{data_text}\n\n"
                f"Computed Metrics:\n{metrics_text}\n\n"
                f"Key Ratios:\n{ratios_text}\n\n"
                "Include these sections:\n"
                "1. Executive Summary\n"
                "2. Revenue & Income Analysis\n"
                "3. Expense Analysis\n"
                "4. Key Financial Ratios & Indicators\n"
                "5. Period-over-Period Comparison\n"
                "6. Outlook & Recommendations"
            ),
        }
    ]

    logger.info("Generating full financial report for %s", period)
    return chat(messages, system_prompt=system_prompt, temperature=0.3, max_tokens=4000)


def generate_executive_summary(metrics: dict, period: str) -> str:
    """Generate a concise executive summary via the LLM.

    Args:
        metrics: Pre-computed financial metrics.
        period: Reporting period label.

    Returns:
        Markdown-formatted executive summary string.
    """
    metrics_text = json.dumps(metrics, indent=2, default=str)

    system_prompt = (
        "You are a CFO writing a brief executive summary. Be concise but insightful. "
        "Highlight key figures and trends. Use markdown formatting."
    )

    messages = [
        {
            "role": "user",
            "content": (
                f"Write a 3-paragraph executive summary for {period}:\n\n"
                f"Key Metrics:\n{metrics_text}"
            ),
        }
    ]

    logger.info("Generating executive summary for %s", period)
    return chat(messages, system_prompt=system_prompt, temperature=0.3, max_tokens=1500)


def generate_cash_flow_narrative(data: list[dict], metrics: dict) -> str:
    """Generate a cash-flow-focused narrative via the LLM.

    Args:
        data: Raw financial rows.
        metrics: Pre-computed financial metrics.

    Returns:
        Markdown-formatted cash flow narrative.
    """
    data_text = "\n".join(str(row) for row in data[:20])
    metrics_text = json.dumps(metrics, indent=2, default=str)

    system_prompt = (
        "You are a treasury analyst. Write a concise cash flow analysis. "
        "Focus on inflows, outflows, net position, and liquidity trends. "
        "Use markdown formatting."
    )

    messages = [
        {
            "role": "user",
            "content": (
                "Analyze the following financial data from a cash flow perspective:\n\n"
                f"Data:\n{data_text}\n\n"
                f"Metrics:\n{metrics_text}"
            ),
        }
    ]

    logger.info("Generating cash flow narrative")
    return chat(messages, system_prompt=system_prompt, temperature=0.3, max_tokens=2000)
