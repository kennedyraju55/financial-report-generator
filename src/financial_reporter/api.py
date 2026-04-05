"""FastAPI REST API for Financial Report Generator."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uvicorn

from financial_reporter.core import (
    compute_financial_metrics,
    compute_ratios,
    compare_periods,
    forecast_metrics,
    generate_financial_report,
    generate_executive_summary,
    generate_cash_flow_narrative,
)

app = FastAPI(
    title="Financial Report Generator API",
    description="REST API for Financial Report Generator",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Request / Response Models
# ---------------------------------------------------------------------------

class FinancialDataRequest(BaseModel):
    data: List[Dict[str, Any]] = Field(..., description="List of financial data records")


class ComputeRatiosRequest(BaseModel):
    metrics: Dict[str, Any] = Field(..., description="Computed financial metrics")


class ComparePeriodsRequest(BaseModel):
    data: List[Dict[str, Any]] = Field(..., description="List of financial data records")
    current_period: str = Field(..., description="Label for the current period")
    previous_period: str = Field(..., description="Label for the previous period")


class ForecastMetricsRequest(BaseModel):
    data: List[Dict[str, Any]] = Field(..., description="List of financial data records")
    periods_ahead: Optional[int] = Field(3, description="Number of periods to forecast ahead")


class GenerateReportRequest(BaseModel):
    data: List[Dict[str, Any]] = Field(..., description="List of financial data records")
    metrics: Dict[str, Any] = Field(..., description="Computed financial metrics")
    period: str = Field(..., description="Reporting period label")


class ExecutiveSummaryRequest(BaseModel):
    metrics: Dict[str, Any] = Field(..., description="Computed financial metrics")
    period: str = Field(..., description="Reporting period label")


class CashFlowNarrativeRequest(BaseModel):
    data: List[Dict[str, Any]] = Field(..., description="List of financial data records")
    metrics: Dict[str, Any] = Field(..., description="Computed financial metrics")


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "financial-report-generator"}


@app.post("/compute-financial-metrics")
async def api_compute_financial_metrics(request: FinancialDataRequest):
    """Compute financial metrics from raw data."""
    try:
        result = compute_financial_metrics(request.data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/compute-ratios")
async def api_compute_ratios(request: ComputeRatiosRequest):
    """Compute financial ratios from metrics."""
    try:
        result = compute_ratios(request.metrics)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/compare-periods")
async def api_compare_periods(request: ComparePeriodsRequest):
    """Compare financial data across two periods."""
    try:
        result = compare_periods(request.data, request.current_period, request.previous_period)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/forecast-metrics")
async def api_forecast_metrics(request: ForecastMetricsRequest):
    """Forecast financial metrics into future periods."""
    try:
        result = forecast_metrics(request.data, periods_ahead=request.periods_ahead)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-financial-report")
async def api_generate_financial_report(request: GenerateReportRequest):
    """Generate a full financial report for a period."""
    try:
        result = generate_financial_report(request.data, request.metrics, request.period)
        return {"report": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-executive-summary")
async def api_generate_executive_summary(request: ExecutiveSummaryRequest):
    """Generate an executive summary from financial metrics."""
    try:
        result = generate_executive_summary(request.metrics, request.period)
        return {"summary": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-cash-flow-narrative")
async def api_generate_cash_flow_narrative(request: CashFlowNarrativeRequest):
    """Generate a narrative around cash flow data."""
    try:
        result = generate_cash_flow_narrative(request.data, request.metrics)
        return {"narrative": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
