"""Data downloader using yfinance API — no WRDS required."""

import yfinance as yf
import pandas as pd
from pathlib import Path
from typing import List, Optional
import time


class DataDownloader:
    """Download price and fundamental data from yfinance."""
    
    def __init__(self, output_path: Optional[Path] = None):
        """
        Initialize downloader.
        
        Args:
            output_path: Root path for raw data. Defaults to data/raw/
        """
        if output_path is None:
            output_path = Path("data/raw")
        
        self.raw_path = output_path
        self.prices_path = self.raw_path / "prices"
        self.fundamentals_path = self.raw_path / "fundamentals"
        
        # Create directories
        self.prices_path.mkdir(parents=True, exist_ok=True)
        self.fundamentals_path.mkdir(parents=True, exist_ok=True)
    
    def download_prices(
        self,
        tickers: List[str],
        start_date: str = "2015-01-01",
        end_date: str = None,
        interval: str = "1mo",
    ) -> pd.DataFrame:
        """
        Download monthly adjusted close prices and calculate returns.
        
        Args:
            tickers: List of ticker symbols (e.g., ['AAPL', 'MSFT', ...])
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD). If None, uses today.
            interval: yfinance interval ('1d', '1wk', '1mo')
        
        Returns:
            DataFrame with columns: date, ticker, adj_close, return
        """
        print(f"Downloading {interval} prices for {len(tickers)} tickers...")
        print(f"Date range: {start_date} to {end_date or 'today'}")
        
        # Download data
        data = yf.download(
            tickers,
            start=start_date,
            end=end_date,
            interval=interval,
            progress=True,
            auto_adjust=False,
        )
        
        # Extract adjusted close prices (fallback to Close if Adj Close is missing)
        if 'Adj Close' in data.columns:
            adj_close = data['Adj Close']
        else:
            adj_close = data['Close']
        
        # Calculate monthly returns
        returns = adj_close.pct_change()
        
        # Reshape from wide to long format
        prices_long = adj_close.stack().reset_index()
        prices_long.columns = ['date', 'ticker', 'adj_close']
        
        returns_long = returns.stack().reset_index()
        returns_long.columns = ['date', 'ticker', 'return']
        
        # Merge prices and returns
        result = prices_long.merge(returns_long, on=['date', 'ticker'])
        
        # Remove NaN returns (first month of each ticker)
        result = result.dropna(subset=['return'])
        
        # Save
        output_file = self.prices_path / "monthly_prices.csv"
        result.to_csv(output_file, index=False)
        print(f"✓ Saved {len(result):,} price observations to {output_file}")
        
        return result
    
    def download_fundamentals(
        self,
        tickers: List[str],
    ) -> pd.DataFrame:
        """
        Download quarterly fundamentals from yfinance.
        
        Args:
            tickers: List of ticker symbols
        
        Returns:
            DataFrame with quarterly balance sheet, income statement, and cash flow data
        """
        print(f"Downloading quarterly fundamentals for {len(tickers)} tickers...")
        
        all_fundamentals = []
        failed_tickers = []
        
        for i, ticker in enumerate(tickers):
            print(f"  [{i+1}/{len(tickers)}] {ticker}...", end=" ")
            
            try:
                stock = yf.Ticker(ticker)
                
                # Get quarterly data
                info = stock.info
                quarterly_financials = stock.quarterly_financials
                
                if quarterly_financials is None or quarterly_financials.empty:
                    print("No data")
                    failed_tickers.append(ticker)
                    continue
                
                # Transpose: dates become rows, items become columns
                df = quarterly_financials.T.reset_index()
                df.columns.name = None
                df = df.rename(columns={'index': 'date'})
                df['ticker'] = ticker
                
                # Add selected fields from info if available
                if 'industry' in info:
                    df['industry'] = info['industry']
                if 'sector' in info:
                    df['sector'] = info['sector']
                if 'marketCap' in info:
                    df['market_cap'] = info['marketCap']
                
                all_fundamentals.append(df)
                print(f"✓ ({len(df)} quarters)")
                
                # Rate limiting to avoid hitting API limits
                time.sleep(0.5)
            
            except Exception as e:
                print(f"Error: {e}")
                failed_tickers.append(ticker)
        
        if failed_tickers:
            print(f"\nFailed to download: {', '.join(failed_tickers)}")
        
        if not all_fundamentals:
            print("No data downloaded")
            return pd.DataFrame()
        
        # Combine
        result = pd.concat(all_fundamentals, ignore_index=True)
        
        # Save
        output_file = self.fundamentals_path / "quarterly_fundamentals.csv"
        result.to_csv(output_file, index=False)
        print(f"✓ Saved {len(result):,} fundamental observations to {output_file}")
        
        return result
    
    @staticmethod
    def load_ticker_list(ticker_file: Path) -> List[str]:
        """
        Load tickers from CSV file.
        
        Expected format:
            ticker
            AAPL
            MSFT
            ...
        
        Args:
            ticker_file: Path to CSV file with tickers
        
        Returns:
            List of ticker symbols
        """
        df = pd.read_csv(ticker_file)
        tickers = df['ticker'].tolist()
        return tickers


def download_sp500_constituents() -> List[str]:
    """
    Download current S&P 500 constituents using yfinance.
    
    Returns:
        List of S&P 500 ticker symbols
    """
    print("Downloading S&P 500 constituents...")
    
    try:
        # yfinance can pull the S&P 500 list
        sp500 = yf.download("^GSPC", start="2024-01-01", end="2024-01-02", progress=False)
        
        # Alternative: manually maintained list or download from Wikipedia
        # For now, return a well-known subset for testing
        sp500_tickers = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA',
            'META', 'TSLA', 'BRK-B', 'JNJ', 'V',
            'JPM', 'WMT', 'PG', 'MA', 'UNH',
            'COST', 'KO', 'PEP', 'AVGO', 'ACN',
        ]
        
        print(f"✓ Loaded {len(sp500_tickers)} S&P 500 tickers (subset)")
        return sp500_tickers
    
    except Exception as e:
        print(f"Error downloading S&P 500 constituents: {e}")
        return []


if __name__ == "__main__":
    # Example usage
    downloader = DataDownloader()
    
    # Download S&P 500 constituents (subset)
    tickers = download_sp500_constituents()
    
    # Download data
    prices = downloader.download_prices(tickers, start_date="2015-01-01")
    fundamentals = downloader.download_fundamentals(tickers)
    
    print("\n✓ Data download complete!")
