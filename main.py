"""Main entry point to run the data download and panel building pipeline."""

import sys
from pathlib import Path

# Add src to python path
sys.path.insert(0, str(Path(__file__).parent))

from src.ingestion.data_downloader import DataDownloader, download_sp500_constituents
from src.panels.build_master import build_master_panel

def main():
    print("Starting Market Structure Lab Data Pipeline...")

    # Initialize downloader
    downloader = DataDownloader()

    # Download S&P 500 constituents subset
    tickers = download_sp500_constituents()

    if not tickers:
        print("❌ Error: No tickers loaded. Exiting.")
        sys.exit(1)

    # Download prices and fundamentals
    print("\n--- Phase 1: Downloading Prices ---")
    downloader.download_prices(tickers, start_date="2015-01-01")

    print("\n--- Phase 2: Downloading Fundamentals ---")
    downloader.download_fundamentals(tickers)

    # Build master panel
    print("\n--- Phase 3: Building Master Panel ---")
    build_master_panel()

    print("\n✅ Data pipeline completed successfully!")

if __name__ == "__main__":
    main()
