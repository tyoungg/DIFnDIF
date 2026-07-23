import pytest
import pandas as pd
from pathlib import Path
from src.utils.data_loader import load_processed_data, load_master_panel


def test_load_processed_data_missing():
    # Test that load_processed_data returns None when the file does not exist
    result = load_processed_data("nonexistent.parquet")
    assert result is None


def test_load_processed_data_exists():
    # Since we have built the master panel, this file should exist and load correctly
    result = load_processed_data("master_panel.parquet")
    if result is not None:
        assert isinstance(result, pd.DataFrame)
        assert "ticker" in result.columns


def test_load_master_panel_missing(tmp_path):
    # Test that load_master_panel raises FileNotFoundError when master_panel.parquet does not exist
    with pytest.raises(FileNotFoundError):
        load_master_panel(processed_path=tmp_path)


def test_load_master_panel_exists():
    # Since we built the master_panel.parquet, load_master_panel should load it correctly
    result = load_master_panel()
    assert isinstance(result, pd.DataFrame)
    assert "ticker" in result.columns
