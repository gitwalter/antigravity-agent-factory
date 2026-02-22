import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
import pandas as pd
import numpy as np
from core.analysis_manager import AnalysisManager


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "x": np.arange(10),
            "y": np.arange(10) * 2 + 1,
            "z": [1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        }
    )


def test_linear_regression(sample_df):
    results = AnalysisManager.run_linear_regression(sample_df, "x", "y")
    assert results is not None
    assert results["r2"] == 1.0
    assert results["coefficient"] == pytest.approx(2.0)
    assert results["intercept"] == pytest.approx(1.0)


def test_correlation_matrix(sample_df):
    corr = AnalysisManager.get_correlation_matrix(sample_df)
    assert corr is not None
    assert corr.shape == (3, 3)
    assert corr.loc["x", "y"] == 1.0


def test_time_series_baseline(sample_df):
    results = AnalysisManager.run_time_series_baseline(sample_df, "y", window=2)
    assert results is not None
    assert len(results["sma"]) == 10
    assert results["latest_sma"] == 18.0  # (17 + 19) / 2
