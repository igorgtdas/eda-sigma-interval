# src/eda_igor/__init__.py
from .eda import assess_normality, outlier_summary, sigma_intervals, run_eda

__all__ = [
    "assess_normality",
    "outlier_summary",
    "sigma_intervals",
    "run_eda",
]