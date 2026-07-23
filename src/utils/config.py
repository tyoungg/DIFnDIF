"""Centralized configuration for paths and parameters."""

from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_ROOT = PROJECT_ROOT / "data"
DATA_RAW = DATA_ROOT / "raw"
DATA_PROCESSED = DATA_ROOT / "processed"
DATA_METADATA = DATA_ROOT / "metadata"

# Create directories if they don't exist
DATA_RAW.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
DATA_METADATA.mkdir(parents=True, exist_ok=True)

# Create subdirectories for raw data
(DATA_RAW / "prices").mkdir(parents=True, exist_ok=True)
(DATA_RAW / "fundamentals").mkdir(parents=True, exist_ok=True)

# Data source: yfinance (no credentials required)
DATA_SOURCE = "yfinance"  # Free API, no auth needed

# Analysis parameters
EVENT_WINDOW = (-36, 60)  # months relative to inclusion
MIN_FIRM_SIZE = 100_000_000  # $100M market cap minimum

# yfinance parameters
YFINANCE_START_DATE = "2015-01-01"
YFINANCE_INTERVAL = "1mo"  # monthly interval

# Matching parameters
MATCHING_CONTROLS = 5
CALIPER = 0.25
