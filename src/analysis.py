"""
Analytical, Econometric, and Forecasting Evaluation Module for Agribusiness Data.

This module provides reusable statistical functions, KPI calculators, time-series
decomposition helpers, and forecast validation metrics for agricultural research.
"""

from typing import Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# 1. Agricultural KPI Calculators
# ---------------------------------------------------------------------------

def calculate_cagr(start_val: float, end_val: float, periods: int) -> float:
    """
    Computes Compound Annual Growth Rate (CAGR).
    Formula: CAGR = ((End_Value / Start_Value) ** (1 / periods)) - 1
    """
    if start_val <= 0 or end_val <= 0 or periods <= 0:
        return np.nan
    return float((end_val / start_val) ** (1.0 / periods) - 1.0)


def calculate_yoy_growth(series: pd.Series) -> pd.Series:
    """
    Calculates Year-over-Year (YoY) percentage growth rate.
    Formula: YoY = ((Value_t - Value_t-1) / Value_t-1) * 100
    """
    return series.pct_change(periods=1) * 100.0


def calculate_price_volatility(
    price_series: pd.Series,
    window: Optional[int] = None,
    annualize: bool = False,
    trading_periods: int = 252
) -> Union[float, pd.Series]:
    """
    Computes commodity price volatility based on the standard deviation of log returns.

    Args:
        price_series: Series of commodity prices.
        window: If specified, returns rolling volatility over window; else scalar overall.
        annualize: If True, multiplies standard deviation by sqrt(trading_periods).
        trading_periods: Scaling factor for annualization (default 252 days or 12 months).

    Returns:
        Union[float, pd.Series]: Volatility metric.
    """
    clean_prices = price_series.dropna()
    log_returns = np.log(clean_prices / clean_prices.shift(1)).dropna()

    scale = np.sqrt(trading_periods) if annualize else 1.0

    if window is not None:
        rolling_vol = log_returns.rolling(window=window).std() * scale
        return rolling_vol
    else:
        return float(log_returns.std() * scale)


def calculate_coefficient_of_variation(series: pd.Series) -> float:
    """
    Computes Coefficient of Variation (CV = (std / mean) * 100).
    Key indicator of relative price and yield instability across commodities and regions.
    """
    clean_series = series.dropna()
    mean_val = clean_series.mean()
    if mean_val == 0 or np.isnan(mean_val):
        return np.nan
    return float((clean_series.std() / mean_val) * 100.0)


def calculate_spatial_yield_index(
    district_yield: float,
    benchmark_yield: float
) -> float:
    """
    Computes Spatial Yield Index (SYI) relative to a benchmark (e.g., State or National mean).
    Formula: SYI = (District_Yield / Benchmark_Yield) * 100
    """
    if benchmark_yield <= 0:
        return np.nan
    return float((district_yield / benchmark_yield) * 100.0)


def calculate_cropping_intensity(gross_cropped_area: float, net_sown_area: float) -> float:
    """
    Computes Cropping Intensity Index.
    Formula: Cropping Intensity (%) = (Gross Cropped Area / Net Sown Area) * 100
    """
    if net_sown_area <= 0:
        return np.nan
    return float((gross_cropped_area / net_sown_area) * 100.0)


# ---------------------------------------------------------------------------
# 2. Statistical Analysis & Time-Series Helpers
# ---------------------------------------------------------------------------

def compute_descriptive_stats(df: pd.DataFrame, numeric_cols: List[str]) -> pd.DataFrame:
    """
    Generates a structured summary of descriptive statistics for selected variables.
    Includes Mean, Median, Std Dev, Variance, IQR, Skewness, and Kurtosis.
    """
    records = []
    for col in numeric_cols:
        if col in df.columns:
            series = pd.to_numeric(df[col], errors="coerce").dropna()
            if len(series) == 0:
                continue
            q25 = float(series.quantile(0.25))
            q75 = float(series.quantile(0.75))
            records.append({
                "Variable": col,
                "Count": int(len(series)),
                "Mean": float(series.mean()),
                "Median": float(series.median()),
                "Std_Dev": float(series.std()),
                "Variance": float(series.var()),
                "IQR": q75 - q25,
                "Min": float(series.min()),
                "Max": float(series.max()),
                "Skewness": float(series.skew()),
                "Kurtosis": float(series.kurtosis()),
            })
    return pd.DataFrame(records)


def perform_stationarity_test(series: pd.Series) -> Dict[str, Union[float, bool, str]]:
    """
    Wrapper for Augmented Dickey-Fuller (ADF) test for time-series stationarity.
    H0: Unit root present (series is non-stationary).
    H1: Series is stationary.
    """
    try:
        from statsmodels.tsa.stattools import adfuller
        clean_series = series.dropna()
        if len(clean_series) < 15:
            return {"error": "Insufficient observations for ADF test"}

        result = adfuller(clean_series, autolag="AIC")
        return {
            "adf_statistic": float(result[0]),
            "p_value": float(result[1]),
            "used_lag": int(result[2]),
            "nobs": int(result[3]),
            "critical_values": {k: float(v) for k, v in result[4].items()},
            "is_stationary": bool(result[1] < 0.05)
        }
    except ImportError:
        return {"error": "statsmodels package not installed"}


# ---------------------------------------------------------------------------
# 3. Forecast Evaluation Metrics
# ---------------------------------------------------------------------------

def mean_absolute_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Computes Mean Absolute Error (MAE)."""
    return float(np.mean(np.abs(y_true - y_pred)))


def root_mean_squared_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Computes Root Mean Squared Error (RMSE)."""
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def mean_absolute_percentage_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Computes Mean Absolute Percentage Error (MAPE).
    Filters out true zero values to prevent division by zero.
    """
    mask = y_true != 0
    if not np.any(mask):
        return np.nan
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100.0)


def symmetric_mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Computes Symmetric Mean Absolute Percentage Error (sMAPE).
    Bounded between 0% and 200%.
    """
    denominator = (np.abs(y_true) + np.abs(y_pred)) / 2.0
    mask = denominator != 0
    if not np.any(mask):
        return np.nan
    return float(np.mean(np.abs(y_pred[mask] - y_true[mask]) / denominator[mask]) * 100.0)


def evaluate_forecast(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Aggregates all standard forecast validation metrics into a single dictionary.
    """
    y_true_arr = np.asarray(y_true, dtype=float)
    y_pred_arr = np.asarray(y_pred, dtype=float)

    return {
        "MAE": mean_absolute_error(y_true_arr, y_pred_arr),
        "RMSE": root_mean_squared_error(y_true_arr, y_pred_arr),
        "MAPE": mean_absolute_percentage_error(y_true_arr, y_pred_arr),
        "sMAPE": symmetric_mape(y_true_arr, y_pred_arr),
    }
