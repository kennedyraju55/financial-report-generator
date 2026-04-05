#!/usr/bin/env python3
"""Financial Report Generator - Rich CLI powered by Click."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

from src.financial_reporter import core

console = Console()


def _require_ollama() -> None:
    """Exit if Ollama is not reachable."""
    if not core.check_ollama_running():
        console.print("[red]Error:[/red] Ollama is not running. Start it with: ollama serve")
        sys.exit(1)


def _display_metrics_table(metrics: dict, currency_symbol: str = "$") -> None:
    """Render a Rich table of financial metrics."""
    table = Table(title="💰 Financial Data Summary", show_lines=True)
    table.add_column("Metric", style="cyan bold", min_width=18)
    table.add_column("Total", justify="right", width=14)
    table.add_column("Average", justify="right", width=14)
    table.add_column("Latest", justify="right", width=14)

    for col, vals in metrics.items():
        table.add_row(
            col,
            f"{currency_symbol}{vals['total']:,.2f}",
            f"{currency_symbol}{vals['average']:,.2f}",
            f"{currency_symbol}{vals['latest']:,.2f}",
        )
    console.print(table)


@click.group()
@click.option("--config", "-c", default="config.yaml", help="Path to config YAML.")
@click.pass_context
def main(ctx: click.Context, config: str) -> None:
    """💰 Financial Report Generator — production-grade CLI."""
    ctx.ensure_object(dict)
    ctx.obj["config"] = core.load_config(config)


@main.command()
@click.option("--file", "-f", "file_path", required=True, help="Path to financial data CSV.")
@click.option("--period", "-p", required=True, help="Reporting period (e.g., Q4-2024).")
@click.option("--full/--summary", default=True, help="Full report or executive summary only.")
@click.pass_context
def report(ctx: click.Context, file_path: str, period: str, full: bool) -> None:
    """Generate a full financial report or executive summary."""
    cfg = ctx.obj["config"]
    console.print(Panel(f"💰 [bold blue]Financial Report Generator — {period}[/bold blue]", expand=False))

    _require_ollama()

    with console.status("[bold green]Loading financial data..."):
        data = core.load_financial_data(file_path)
    console.print(f"[green]✓[/green] Loaded [bold]{len(data)}[/bold] records from [bold]{file_path}[/bold]\n")

    with console.status("[bold green]Computing financial metrics..."):
        metrics = core.compute_financial_metrics(data)

    _display_metrics_table(metrics, cfg.get("currency_symbol", "$"))
    console.print()

    if full:
        with console.status("[bold green]Generating financial report..."):
            report_text = core.generate_financial_report(data, metrics, period)
        console.print(Panel(Markdown(report_text), title=f"📋 Financial Report — {period}", border_style="green"))
    else:
        with console.status("[bold green]Generating executive summary..."):
            summary_text = core.generate_executive_summary(metrics, period)
        console.print(Panel(Markdown(summary_text), title=f"📋 Executive Summary — {period}", border_style="green"))


@main.command()
@click.option("--file", "-f", "file_path", required=True, help="Path to financial data CSV.")
@click.option("--period", "-p", required=True, help="Reporting period.")
def summary(file_path: str, period: str) -> None:
    """Generate an executive summary only."""
    _require_ollama()

    data = core.load_financial_data(file_path)
    metrics = core.compute_financial_metrics(data)

    with console.status("[bold green]Generating executive summary..."):
        text = core.generate_executive_summary(metrics, period)
    console.print(Panel(Markdown(text), title=f"📋 Executive Summary — {period}", border_style="blue"))


@main.command()
@click.option("--file", "-f", "file_path", required=True, help="Path to financial data CSV.")
def ratios(file_path: str) -> None:
    """Display financial ratio analysis."""
    data = core.load_financial_data(file_path)
    metrics = core.compute_financial_metrics(data)
    ratio_data = core.compute_ratios(metrics)

    table = Table(title="📊 Financial Ratio Analysis", show_lines=True)
    table.add_column("Ratio", style="cyan bold", min_width=20)
    table.add_column("Value", justify="right", width=14)

    for name, value in ratio_data.items():
        label = name.replace("_", " ").title()
        table.add_row(label, f"{value:.2%}")

    console.print(table)


@main.command()
@click.option("--file", "-f", "file_path", required=True, help="Path to financial data CSV.")
@click.option("--periods", "-n", default=3, help="Number of periods to forecast.")
def forecast(file_path: str, periods: int) -> None:
    """Show forecasted financial metrics."""
    data = core.load_financial_data(file_path)
    forecasts = core.forecast_metrics(data, periods_ahead=periods)

    table = Table(title="🔮 Financial Forecast", show_lines=True)
    table.add_column("Metric", style="cyan bold", min_width=18)
    for i in range(1, periods + 1):
        table.add_column(f"Period +{i}", justify="right", width=14)

    for col, values in forecasts.items():
        table.add_row(col, *[f"${v:,.2f}" for v in values])

    console.print(table)


if __name__ == "__main__":
    main()
