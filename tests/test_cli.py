"""Tests for financial_reporter.cli — Click CLI commands."""

import os
import sys

import pytest
from unittest.mock import patch
from click.testing import CliRunner

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.financial_reporter.cli import main


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
def runner():
    return CliRunner()


# ---------------------------------------------------------------------------
# Report command
# ---------------------------------------------------------------------------

class TestReportCommand:
    @patch("src.financial_reporter.core.check_ollama_running", return_value=True)
    @patch("src.financial_reporter.core.chat")
    def test_full_report(self, mock_chat, mock_check, runner, sample_financials_csv):
        mock_chat.return_value = "# Financial Report\n\nStrong Q4 performance..."
        result = runner.invoke(main, ["report", "--file", sample_financials_csv, "--period", "Q4-2024"])
        assert result.exit_code == 0

    @patch("src.financial_reporter.core.check_ollama_running", return_value=True)
    @patch("src.financial_reporter.core.chat")
    def test_summary_only(self, mock_chat, mock_check, runner, sample_financials_csv):
        mock_chat.return_value = "## Executive Summary\n\nSolid quarter."
        result = runner.invoke(main, ["report", "--file", sample_financials_csv, "--period", "Q4-2024", "--summary"])
        assert result.exit_code == 0

    @patch("src.financial_reporter.core.check_ollama_running", return_value=False)
    def test_ollama_not_running(self, mock_check, runner, sample_financials_csv):
        result = runner.invoke(main, ["report", "--file", sample_financials_csv, "--period", "Q4-2024"])
        assert result.exit_code != 0


# ---------------------------------------------------------------------------
# Summary command
# ---------------------------------------------------------------------------

class TestSummaryCommand:
    @patch("src.financial_reporter.core.check_ollama_running", return_value=True)
    @patch("src.financial_reporter.core.chat")
    def test_summary(self, mock_chat, mock_check, runner, sample_financials_csv):
        mock_chat.return_value = "## Summary\n\nGood quarter."
        result = runner.invoke(main, ["summary", "--file", sample_financials_csv, "--period", "Q4-2024"])
        assert result.exit_code == 0


# ---------------------------------------------------------------------------
# Ratios command
# ---------------------------------------------------------------------------

class TestRatiosCommand:
    def test_ratios(self, runner, sample_financials_csv):
        result = runner.invoke(main, ["ratios", "--file", sample_financials_csv])
        assert result.exit_code == 0
        assert "Profit Margin" in result.output or "Ratio" in result.output


# ---------------------------------------------------------------------------
# Forecast command
# ---------------------------------------------------------------------------

class TestForecastCommand:
    def test_forecast(self, runner, sample_financials_csv):
        result = runner.invoke(main, ["forecast", "--file", sample_financials_csv])
        assert result.exit_code == 0

    def test_forecast_custom_periods(self, runner, sample_financials_csv):
        result = runner.invoke(main, ["forecast", "--file", sample_financials_csv, "--periods", "5"])
        assert result.exit_code == 0
