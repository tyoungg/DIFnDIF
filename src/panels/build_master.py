"""Build master panel by merging prices and fundamentals."""

import pandas as pd
from pathlib import Path
from typing import Optional


def build_master_panel(
    raw_path: Optional[Path] = None,
    processed_path: Optional[Path] = None,
) -> pd.DataFrame:
    """
    Merge monthly prices with quarterly fundamentals into a single panel.
    
    Key technique: merge_asof with direction='backward' prevents look-ahead bias
    by matching each monthly return with the most recent quarterly fundamental report.
    
    Args:
        raw_path: Path to raw data directory. Defaults to data/raw/
        processed_path: Path to processed data directory. Defaults to data/processed/
    
    Returns:
        Master panel DataFrame
    """
    if raw_path is None:
        raw_path = Path("data/raw")
    if processed_path is None:
        processed_path = Path("data/processed")
    
    processed_path.mkdir(parents=True, exist_ok=True)
    
    print("Building master panel...")
    
    # Load data
    print("  Loading prices...")
    prices = pd.read_csv(raw_path / "prices" / "monthly_prices.csv")
    prices['date'] = pd.to_datetime(prices['date'])
    
    print("  Loading fundamentals...")
    fundamentals = pd.read_csv(raw_path / "fundamentals" / "quarterly_fundamentals.csv")
    fundamentals['date'] = pd.to_datetime(fundamentals['date'])
    
    # Sort globally by date (required for merge_asof)
    prices = prices.sort_values('date').reset_index(drop=True)
    fundamentals = fundamentals.sort_values('date').reset_index(drop=True)
    
    print("  Merging prices with fundamentals...")
    # The "Magic": merge_asof matches each monthly price with the most recent
    # quarterly fundamental report BEFORE that date, preventing look-ahead bias
    master_panel = pd.merge_asof(
        prices,
        fundamentals,
        on='date',
        by='ticker',
        direction='backward',  # Use last known quarter
        suffixes=('_price', '_fund'),
    )
    
    # Sort final panel
    master_panel = master_panel.sort_values(['ticker', 'date']).reset_index(drop=True)
    
    # Calculate valuation metrics
    print("  Calculating valuation metrics...")
    
    # P/E Ratio: Price / Earnings Per Share
    if 'Diluted Net Income Per Share' in master_panel.columns:
        master_panel['pe_ratio'] = (
            master_panel['adj_close'] / master_panel['Diluted Net Income Per Share']
        )
    
    # Price-to-Sales
    if 'Total Revenue' in master_panel.columns and 'market_cap' in master_panel.columns:
        master_panel['ps_ratio'] = (
            master_panel['market_cap'] / master_panel['Total Revenue']
        )
    
    # Save as Parquet
    output_file = processed_path / "master_panel.parquet"
    master_panel.to_parquet(output_file, index=False)
    
    print(f"✓ Master panel created")
    print(f"  Rows: {len(master_panel):,}")
    print(f"  Columns: {len(master_panel.columns)}")
    print(f"  Tickers: {master_panel['ticker'].nunique()}")
    print(f"  Date range: {master_panel['date'].min().date()} to {master_panel['date'].max().date()}")
    print(f"  Saved to: {output_file}")
    
    return master_panel


if __name__ == "__main__":
    build_master_panel()
