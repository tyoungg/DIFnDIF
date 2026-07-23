"""Utility functions for data loading and processing."""

import pandas as pd
from pathlib import Path
from typing import Optional


def load_processed_data(filename: str):
    """Centralized loader for the Streamlit app to access processed parquet files."""
    # This looks for the file in the project root /data/processed/ folder
    path = Path(__file__).parent.parent.parent / "data" / "processed" / filename

    if not path.exists():
        return None

    try:
        return pd.read_parquet(path)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None


def load_master_panel(processed_path: Optional[Path] = None) -> pd.DataFrame:
    """
    Load the master panel.
    
    Args:
        processed_path: Path to processed data directory. Defaults to data/processed/
    
    Returns:
        Master panel DataFrame
    """
    if processed_path is None:
        processed_path = Path("data/processed")
    
    file_path = processed_path / "master_panel.parquet"
    
    if not file_path.exists():
        raise FileNotFoundError(
            f"Master panel not found at {file_path}. "
            "Run 'make data' to download and build it."
        )
    
    return pd.read_parquet(file_path)


def load_prices(raw_path: Optional[Path] = None) -> pd.DataFrame:
    """Load monthly prices."""
    if raw_path is None:
        raw_path = Path("data/raw")
    
    file_path = raw_path / "prices" / "monthly_prices.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"Prices not found at {file_path}")
    
    return pd.read_csv(file_path)


def load_fundamentals(raw_path: Optional[Path] = None) -> pd.DataFrame:
    """Load quarterly fundamentals."""
    if raw_path is None:
        raw_path = Path("data/raw")
    
    file_path = raw_path / "fundamentals" / "quarterly_fundamentals.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"Fundamentals not found at {file_path}")
    
    return pd.read_csv(file_path)
