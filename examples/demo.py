"""
Demo script for Financial Report Generator
Shows how to use the core module programmatically.

Usage:
    python examples/demo.py
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.financial_reporter.core import load_config, safe_float, load_financial_data, compute_financial_metrics, compute_ratios, compare_periods, forecast_metrics, compute_analytics, generate_financial_report, generate_executive_summary


def main():
    """Run a quick demo of Financial Report Generator."""
    print("=" * 60)
    print("🚀 Financial Report Generator - Demo")
    print("=" * 60)
    print()
    # Load configuration from a YAML file, falling back to defaults.
    print("📝 Example: load_config()")
    result = load_config()
    print(f"   Result: {result}")
    print()
    # Convert a value to float, stripping currency/percentage symbols.
    print("📝 Example: safe_float()")
    result = safe_float(
        val="sample data"
    )
    print(f"   Result: {result}")
    print()
    # Load financial data from a CSV file.
    print("📝 Example: load_financial_data()")
    result = load_financial_data(
        file_path="sample.txt"
    )
    print(f"   Result: {result}")
    print()
    # Compute key financial metrics (total, average, min, max, latest)
    print("📝 Example: compute_financial_metrics()")
    result = compute_financial_metrics(
        data=[{"key": "value"}]
    )
    print(f"   Result: {result}")
    print()
    print("✅ Demo complete! See README.md for more examples.")


if __name__ == "__main__":
    main()
