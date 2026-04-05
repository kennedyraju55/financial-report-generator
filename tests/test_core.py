"""Tests for financial_reporter.core — business logic."""

import json
import os
import sys

import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.financial_reporter.core import (
    load_financial_data,
    safe_float,
    compute_financial_metrics,
    compute_ratios,
    compare_periods,
    forecast_metrics,
    generate_financial_report,
    generate_executive_summary,
    generate_cash_flow_narrative,
    load_config,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_financials_csv(tmp_path):
    """Create a sample financial data CSV."""
    csv_path = tmp_path / "financials.csv"
    csv_path.write_text(
        "month,revenue,expenses,net_income\n"
        "October,500000,350000,150000\n"
        "November,550000,380000,170000\n"
        "December,600000,400000,200000\n"
    )
    return str(csv_path)


@pytest.fixture
def sample_financial_data():
    """Return sample financial data as list of dicts."""
    return [
        {"month": "Oct", "revenue": "500000", "expenses": "350000", "net_income": "150000"},
        {"month": "Nov", "revenue": "550000", "expenses": "380000", "net_income": "170000"},
        {"month": "Dec", "revenue": "600000", "expenses": "400000", "net_income": "200000"},
    ]


@pytest.fixture
def sample_metrics(sample_financial_data):
    return compute_financial_metrics(sample_financial_data)


# ---------------------------------------------------------------------------
# TestLoadFinancialData
# ---------------------------------------------------------------------------

class TestLoadFinancialData:
    def test_load_valid_csv(self, sample_financials_csv):
        data = load_financial_data(sample_financials_csv)
        assert len(data) == 3
        assert "revenue" in data[0]

    def test_load_nonexistent_file(self):
        with pytest.raises(FileNotFoundError):
            load_financial_data("nonexistent.csv")

    def test_load_empty_csv(self, tmp_path):
        empty = tmp_path / "empty.csv"
        empty.write_text("month,revenue\n")
        with pytest.raises(ValueError, match="empty"):
            load_financial_data(str(empty))


# ---------------------------------------------------------------------------
# TestSafeFloat
# ---------------------------------------------------------------------------

class TestSafeFloat:
    def test_plain_number(self):
        assert safe_float("12345") == 12345.0

    def test_currency_string(self):
        assert safe_float("$1,234.56") == 1234.56

    def test_percentage(self):
        assert safe_float("45.5%") == 45.5

    def test_invalid(self):
        assert safe_float("N/A") == 0.0

    def test_none(self):
        assert safe_float(None) == 0.0


# ---------------------------------------------------------------------------
# TestComputeFinancialMetrics
# ---------------------------------------------------------------------------

class TestComputeFinancialMetrics:
    def test_metrics_computation(self, sample_financial_data):
        metrics = compute_financial_metrics(sample_financial_data)
        assert "revenue" in metrics
        assert metrics["revenue"]["total"] == 1650000
        assert metrics["revenue"]["latest"] == 600000

    def test_metrics_average(self, sample_financial_data):
        metrics = compute_financial_metrics(sample_financial_data)
        assert metrics["net_income"]["average"] == pytest.approx(173333.33, rel=1e-2)

    def test_metrics_min_max(self, sample_financial_data):
        metrics = compute_financial_metrics(sample_financial_data)
        assert metrics["expenses"]["min"] == 350000
        assert metrics["expenses"]["max"] == 400000

    def test_empty_data(self):
        assert compute_financial_metrics([]) == {}


# ---------------------------------------------------------------------------
# TestComputeRatios
# ---------------------------------------------------------------------------

class TestComputeRatios:
    def test_ratios_present(self, sample_metrics):
        ratios = compute_ratios(sample_metrics)
        assert "profit_margin" in ratios
        assert "expense_ratio" in ratios
        assert "operating_margin" in ratios
        assert "growth_rate" in ratios

    def test_profit_margin_value(self, sample_metrics):
        ratios = compute_ratios(sample_metrics)
        # net_income total = 520000, revenue total = 1650000
        expected = 520000 / 1650000
        assert ratios["profit_margin"] == pytest.approx(expected, rel=1e-3)

    def test_expense_ratio_value(self, sample_metrics):
        ratios = compute_ratios(sample_metrics)
        expected = 1130000 / 1650000
        assert ratios["expense_ratio"] == pytest.approx(expected, rel=1e-3)

    def test_empty_metrics(self):
        assert compute_ratios({}) == {}


# ---------------------------------------------------------------------------
# TestComparePeriods
# ---------------------------------------------------------------------------

class TestComparePeriods:
    def test_compare_known_periods(self):
        data = [
            {"month": "Oct", "revenue": "500000", "expenses": "350000", "net_income": "150000"},
            {"month": "Nov", "revenue": "550000", "expenses": "380000", "net_income": "170000"},
        ]
        result = compare_periods(data, "Nov", "Oct")
        assert "current" in result
        assert "previous" in result
        assert "changes" in result

    def test_compare_missing_period(self):
        data = [
            {"month": "Oct", "revenue": "500000", "expenses": "350000", "net_income": "150000"},
        ]
        result = compare_periods(data, "Oct", "Jan")
        assert result["previous"] == {}


# ---------------------------------------------------------------------------
# TestForecastMetrics
# ---------------------------------------------------------------------------

class TestForecastMetrics:
    def test_forecast_length(self, sample_financial_data):
        fc = forecast_metrics(sample_financial_data, periods_ahead=3)
        assert "revenue" in fc
        assert len(fc["revenue"]) == 3

    def test_forecast_increasing_trend(self, sample_financial_data):
        fc = forecast_metrics(sample_financial_data, periods_ahead=1)
        # Revenue is increasing (500k → 550k → 600k), forecast should be > 600k
        assert fc["revenue"][0] > 600000

    def test_forecast_empty_data(self):
        assert forecast_metrics([]) == {}


# ---------------------------------------------------------------------------
# TestGenerateReport
# ---------------------------------------------------------------------------

class TestGenerateReport:
    @patch("src.financial_reporter.core.chat")
    def test_generate_report(self, mock_chat, sample_financial_data):
        mock_chat.return_value = "# Q4-2024 Financial Report\n\nRevenue grew 20%..."
        metrics = compute_financial_metrics(sample_financial_data)
        report = generate_financial_report(sample_financial_data, metrics, "Q4-2024")
        assert "Q4-2024" in report or "Revenue" in report
        mock_chat.assert_called_once()

    @patch("src.financial_reporter.core.chat")
    def test_generate_executive_summary(self, mock_chat, sample_financial_data):
        mock_chat.return_value = "## Executive Summary\n\nStrong quarter."
        metrics = compute_financial_metrics(sample_financial_data)
        text = generate_executive_summary(metrics, "Q4-2024")
        assert len(text) > 0
        mock_chat.assert_called_once()

    @patch("src.financial_reporter.core.chat")
    def test_generate_cash_flow_narrative(self, mock_chat, sample_financial_data):
        mock_chat.return_value = "## Cash Flow\n\nPositive net cash position."
        metrics = compute_financial_metrics(sample_financial_data)
        text = generate_cash_flow_narrative(sample_financial_data, metrics)
        assert "Cash Flow" in text
        mock_chat.assert_called_once()


# ---------------------------------------------------------------------------
# TestLoadConfig
# ---------------------------------------------------------------------------

class TestLoadConfig:
    def test_default_config(self):
        cfg = load_config(None)
        assert cfg["currency"] == "USD"
        assert cfg["model"]["name"] == "gemma3"

    def test_load_yaml(self, tmp_path):
        cfg_path = tmp_path / "test_config.yaml"
        cfg_path.write_text("currency: EUR\ncurrency_symbol: 'E'\n", encoding="utf-8")
        cfg = load_config(str(cfg_path))
        assert cfg["currency"] == "EUR"
        assert cfg["currency_symbol"] == "E"
        # defaults still present
        assert cfg["model"]["name"] == "gemma3"
